# Production-Ready Arabic NLP Preprocessing Pipeline

An optimized, object-oriented Arabic Natural Language Processing (NLP) preprocessing pipeline built with Python and `camel_tools`. Designed for efficiency, memory safety, and high-precision morphological disambiguation prior to feature extraction or model training.

## Key Features

* **Single-Initialization Architecture:** Heavy ML resources (`MLEDisambiguator`) are loaded strictly once during initialization $O(1)$ to minimize runtime overhead and prevent RAM saturation during inference loops.
* **Regex Pre-compilation:** Pre-compiled regular expressions for pattern matching and stripping noise efficiently across large text streams.
* **Noise Cleaning & Text Normalization:** Automated stripping of URLs, non-Arabic tokens, and punctuation, combined with Arabic character normalization (Alif, Tatweel/Kashida, Ta-Marbuta handling).
* **Morphological Disambiguation:** Full support for CAMeL Tools' `atbtok` and `bwtok` schemes, offering both standard tokenization and full prefix/suffix morphological splitting.
* **Encapsulated Private Methods:** Strict boundary separation between private helper utilities (`_remove_noise`, `_morphological_process`) and the clean external execution API (`process`).

---

## Architecture & Data Flow

```text
Raw Text ➔ Noise Removal ➔ Normalization ➔ Simple Split ➔ Morphological Disambiguation ➔ Clean Tokens
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/arabic-nlp-pipeline.git](https://github.com/your-username/arabic-nlp-pipeline.git)
   cd arabic-nlp-pipeline
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download required CAMeL Tools packages:**
   ```bash
   camel_data -i morphology-db-msa-r13
   camel_data -i disambig-mle-msa-r13
   ```

---

## Quickstart Usage

```python
from arabic_nlp_pipeline.pipeline import ArabicNLPipeline

# 1. Instantiate the pipeline (Loads models once into memory)
pipeline = ArabicNLPipeline(scheme='atbtok', split=True)

# 2. Process raw text
dirty_text = "مرحـــبـــاً! وسيلعبون بسياراتهم 🚙 غداً في شارع 99... [https://test.com](https://test.com)"
tokens = pipeline.process(dirty_text)

print(tokens)
# Output: ['مرحبا', 'و+', 'س+', 'يلعبون', 'ب+', 'سيار', 'غدا', 'في', 'شارع']
```

---

## Method Breakdown

| Method | Access | Purpose |
| :--- | :--- | :--- |
| `__init__` | Public | Pre-loads heavy models, compiles regexes, and configures scheme routing. |
| `process` | Public | The single entry point accepting raw text and executing the sequential steps. |
| `_remove_noise` | Private | Cleans URLs, non-Arabic alphanumeric noise, and extra whitespace. |
| `_normalize` | Private | Standardizes character forms (Alif variants, removal of Kashida). |
| `_simple_tokenize` | Private | Performs baseline space-based string splitting. |
| `_morphological_process` | Private | Applies ML disambiguation and handles morphological splitting/dediacritization. |

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
