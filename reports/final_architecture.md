# Final Architecture: TrustSupport Customer Support Agent

The TrustSupport system is an ML-powered, evidence-grounded generative AI customer support agent. It enforces safety and determinism via a hybrid architecture separating semantic classification, risk detection, historical evidence retrieval, and reply generation.

```mermaid
flowchart TD
    Q[Customer Query] --> Classify[Intent Classifier & Risk Detection]
    
    subgraph Phase 5: NLP Router
        Classify --> CheckRisk{High Risk?}
        CheckRisk -- Yes --> ESCALATE[Escalate to Human]
        CheckRisk -- No --> CheckOOD{Out of Domain?}
        CheckOOD -- Yes --> ABSTAIN[Abstain & Fallback]
        CheckOOD -- No --> R[Evidence Retriever]
    end
    
    subgraph Phase 6: FAISS Evidence
        R --> Index[(FAISS Index)]
        Index --> TopK[Top 3 Historical Brand Responses]
        TopK --> ScoreBoost[Intent & Risk Boost]
        ScoreBoost --> FilterDups[Jaccard Deduplication]
    end
    
    FilterDups --> Router[Reply Mode Router]
    
    subgraph Phase 7: Generative Engine
        Router -- GROUNDED_REPLY --> Gemini[Google Gemini API]
        Router -- CAUTIOUS_REPLY --> Gemini
        Router -- CLARIFY --> Template[Deterministic Template]
        
        Gemini --> Safety[Safety Validator]
        Safety -- PASS --> Output[Final Reply Payload]
        Safety -- FAIL (Hallucination) --> Template
    end
    
    Template --> Output
    ABSTAIN --> Output
    ESCALATE --> Output
```

## System Components

### 1. Intent Classification (Phase 5)
- **Model**: `all-MiniLM-L6-v2` SentenceTransformer embeddings + Logistic Regression classifier.
- **Taxonomy**: 13 granular gaming support intents (e.g., `CONNECTION_AND_TECHNICAL`, `PURCHASE_AND_BILLING`).
- **OOD Detection**: Centroid Distance Thresholding.

### 2. Deterministic Risk Detection
- **Mechanism**: Rule-based regex scanning against `BAN_APPEAL` and `LEGAL_THREAT` dictionaries.
- **Function**: Operates orthogonally to semantic intent to guarantee business-critical locks and immediate escalation.

### 3. Evidence Retrieval (Phase 6)
- **Index**: `FAISS IndexFlatIP` (384 dimensions, L2 Normalized).
- **Corpus**: `intent_train.jsonl` (Historical ATVIAssist brand responses).
- **Retrieval Pipeline**:
  - Global Top-20 Cosine Similarity.
  - +0.05 score boost for intent alignment.
  - +0.05 score boost for risk flag alignment.
  - Jaccard Similarity (>0.8) deduplication.
  - Hard cutoff at 0.40 raw similarity.

### 4. Generative Engine & Fallback (Phase 7)
- **Primary Generator**: `gemini-3.5-flash` using `google-genai` SDK.
- **System Prompting**: Contextualized strictly using retrieved evidence metadata, blocking assumptions, promises, or URL generation without evidence.
- **Fallback Generator**: If the Gemini API fails, API keys are missing, or the `SafetyValidator` catches a hallucination, a zero-latency `TemplateGenerator` takes over to provide a safe, non-hallucinated response mapped to the predicted intent.

### 5. Provenance & Safety
- **Safety Validator**: Strict regex post-processing filter. Blocks unauthorized promises ("refund", "unban", "guarantee") and external URLs not explicitly contained in the retrieved historical evidence.
- **Payload**: The system returns a comprehensive JSON structure that guarantees complete observability:
  ```json
  {
      "reply_text": "...",
      "reply_mode": "GROUNDED_REPLY",
      "intent": "PURCHASE_AND_BILLING",
      "generation_source": "GEMINI_API",
      "fallback_used": false,
      "safety_validation": {"passed": true, "reason": "No policy violations"}
  }
  ```
