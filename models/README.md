# Model Storage Layout

Store trained model artifacts in this top-level `models/` folder (not inside `app/models`, which is for Python schema code).

Recommended structure:

- `models/intent/` -> intent classification model files
- `models/nlp/` -> NLP/translation model files
- `models/shared/` -> shared tokenizers, label maps, embeddings

Examples:

- `models/intent/model.joblib`
- `models/intent/labels.json`
- `models/nlp/translator.onnx`
- `models/shared/tokenizer.json`

Notes:

- Large model binaries should usually be excluded from git.
- Keep only small metadata/config files in source control when possible.
- `app/models/` should continue to contain Python classes/schemas only.
