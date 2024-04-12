# Evaluating Toxicity in Knowledge Graphs and its Effects in Downstream Tasks

## Description

This repository accompanies my dissertation titled *'Evaluating Toxicity in Knowledge Graphs and its effect in Downstream Tasks'*. This project evaluates the toxicity of triples in [Wikidata](https://wikidata.org) by verbalising the triples using WDV, and then analysing the toxicity of the verbalisatin using the Perspective API. The downstream tasks examined are KGQA and Link Prediction, both implemented using LLMs.



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

* pip
  ```sh
  python3 -m pip install --upgrade pip
  ```

### Installation

1. Set up accounts and get a free API Keys from: (billing details required)
    OpenAI: https://platform.openai.com/
    Llama: https://www.llama-api.com/
    Mistral Ai: https://mistral.ai/
    Ai21: https://www.ai21.com/studio

2. Clone the repo with its submodules
   ```sh
   git clone --recurse-submodules https://github.com/estherokusanya/wikidata-toxicity.git
   ```
3. Follow steps in [WDV](https://github.com/gabrielmaia7/WDV/tree/13810bd80e2c64956018b5ae508f6eb582deaf3c/Verbalisation) to unpack *graph2text*
4. Update package location in `verbalisation_module.py`
    ```python
        DATA_DIR = 'helpers/WDV/verbalisation/graph2text/data/webnlg'
        OUTPUT_DIR = 'helpers/WDV/verbalisation/graph2text/outputs/test_model'
        CHECKPOINT = 'helpers/WDV/verbalisation/graph2text/outputs/t5-base_13881/val_avg_bleu=68.1000-step_count=5.ckpt'
    ```
3. (Optional) Create a virtual environment
   ```sh
   python3 -m venv <name_of_virtualenv>
   ```
4. Install dependencies from .requirements file
    ```sh
   pip install -r requirements.txt
   ```
5. Store your API keys in `.env`
   ```js
    OPENAI_KEY = 'ENTER YOUR API KEY'
    LLAMA_KEY= ''
    JURASSIC_KEY = ''
    MISTRAL_KEY= ''
    PERSPECTIVEAPI_KEY= ''
   ```




## Author

ex. Esther Okusanya (boluwatife.okusanya@kcl.ac.uk)


## Version History

* 0.1
    * Initial Release


## Acknowledgments

* [readme template](https://github.com/matiassingers/awesome-readme)
* [WDV](https://github.com/gabrielmaia7/WDV)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
