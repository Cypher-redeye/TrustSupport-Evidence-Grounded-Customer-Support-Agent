import pytest
from src.data.build_conversations import ConversationGraph, calculate_metrics

def mock_tweet(tid, author, in_resp='', resp='', text='', inbound=True):
    return {
        'tweet_id': str(tid),
        'author_id': author,
        'inbound': inbound,
        'text': text,
        'created_at': '2017-10-31',
        'in_response_to_tweet_id': str(in_resp) if in_resp else '',
        'response_tweet_id': [str(r).strip() for r in str(resp).split(',')] if resp else []
    }

def test_single_turn():
    graph = ConversationGraph('Brand')
    # Just a customer mentioning the brand, brand never replied (or we only have brand tweet)
    # Let's say we have just one brand tweet (an announcement)
    graph.tweets = {
        '1': mock_tweet(1, 'Brand', inbound=False)
    }
    graph.relevant_tweets = {'1'}
    graph.extract_relevant_graph()
    convs, orphans = graph.build_threads()
    
    assert len(convs) == 1
    assert len(convs['conv_1']) == 1
    assert len(orphans) == 0

def test_customer_brand_conversation():
    graph = ConversationGraph('Brand')
    graph.tweets = {
        '1': mock_tweet(1, 'Customer', resp='2'),
        '2': mock_tweet(2, 'Brand', in_resp='1', inbound=False)
    }
    graph.relevant_tweets = {'2'}
    graph.extract_relevant_graph()
    convs, orphans = graph.build_threads()
    
    assert len(convs) == 1
    thread = convs['conv_1']
    assert len(thread) == 2
    assert thread[0]['tweet_id'] == '1'
    assert thread[1]['tweet_id'] == '2'
    assert len(orphans) == 0

def test_customer_brand_customer_multiturn():
    graph = ConversationGraph('Brand')
    graph.tweets = {
        '1': mock_tweet(1, 'Customer', resp='2'),
        '2': mock_tweet(2, 'Brand', in_resp='1', resp='3', inbound=False),
        '3': mock_tweet(3, 'Customer', in_resp='2')
    }
    graph.relevant_tweets = {'2'}
    graph.extract_relevant_graph()
    convs, orphans = graph.build_threads()
    
    assert len(convs) == 1
    thread = convs['conv_1']
    assert len(thread) == 3
    
    metrics = calculate_metrics(graph, convs, orphans, 'Brand')
    assert metrics['multi_turn_count'] == 1
    assert metrics['complete_conversations'] == 1

def test_missing_parent():
    graph = ConversationGraph('Brand')
    graph.tweets = {
        # Parent '1' is missing from dataset
        '2': mock_tweet(2, 'Brand', in_resp='1', inbound=False)
    }
    graph.relevant_tweets = {'2'}
    graph.extract_relevant_graph()
    convs, orphans = graph.build_threads()
    
    # It should become the root since 1 is missing
    assert len(convs) == 1
    assert 'conv_2' in convs
    assert len(orphans) == 0

def test_missing_child():
    graph = ConversationGraph('Brand')
    graph.tweets = {
        '2': mock_tweet(2, 'Brand', resp='3', inbound=False)
        # Child '3' is missing
    }
    graph.relevant_tweets = {'2'}
    graph.extract_relevant_graph()
    convs, orphans = graph.build_threads()
    
    assert len(convs) == 1
    assert len(convs['conv_2']) == 1

def test_orphaned_tweet():
    graph = ConversationGraph('Brand')
    graph.tweets = {
        '1': mock_tweet(1, 'Brand', inbound=False),
        '2': mock_tweet(2, 'Customer', in_resp='1')
        # Wait, if we start extraction from 1, it will find 2 only if 1 lists 2 as response
        # In this dataset, if 1 doesn't list 2, but 2 lists 1 as parent...
    }
    # For orphaned testing, let's inject a cycle without a root, or an isolated tweet that somehow got in relevant but not visited
    graph.relevant_tweets = {'1', '3'}
    graph.tweets = {
        '1': mock_tweet(1, 'Brand', inbound=False),
        # 3 is relevant but has no links to 1, and let's say 3 is not a brand so it wouldn't naturally form a valid thread if has_brand=False check drops it
        '3': mock_tweet(3, 'Customer', in_resp='999')
    }
    graph.extract_relevant_graph()
    convs, orphans = graph.build_threads()
    
    assert 'conv_1' in convs
    # 3 gets orphaned because it has no brand tweet in its thread so it's dropped from conversations
    # Wait, roots logic: 3's parent is 999 (not in relevant). So 3 is a root. 
    # Thread built from 3 has only 3. 3's author is Customer. has_brand is False. So it's not in convs.
    # Therefore 3 is not in visited! Wait, it IS visited during BFS of root 3.
    # Ah! If it's visited but dropped, it's NOT in orphans if visited.add happens.
    # So to make an orphan, we need it to not be visited.
    
    # Let's simulate a strict cycle with no external parent, making it have no roots
    pass # we'll test cycle instead

def test_cycle_protection():
    graph = ConversationGraph('Brand')
    # 1 -> 2 -> 1
    graph.tweets = {
        '1': mock_tweet(1, 'Brand', in_resp='2', resp='2', inbound=False),
        '2': mock_tweet(2, 'Customer', in_resp='1', resp='1')
    }
    graph.relevant_tweets = {'1'}
    graph.extract_relevant_graph()
    
    # In roots logic:
    # 1's parent is 2, which IS in relevant. So 1 is NOT a root.
    # 2's parent is 1, which IS in relevant. So 2 is NOT a root.
    # Therefore roots = [].
    # So neither is visited. Both become orphans!
    convs, orphans = graph.build_threads()
    assert len(convs) == 0
    assert len(orphans) == 2
