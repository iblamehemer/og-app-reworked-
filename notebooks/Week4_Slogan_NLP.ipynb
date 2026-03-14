{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "colab": {
   "provenance": []
  }
 },
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# \u270d BrandMind AI \u2014 Week 4\n## Creative Content Hub \u2014 Tagline & Slogan Generation\n**Tools:** Gemini API \u00b7 HuggingFace Transformers \u00b7 NLTK"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "!pip install google-generativeai nltk transformers pandas -q"
   ],
   "outputs": [],
   "execution_count": null
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import nltk, re, json, pandas as pd\nnltk.download(['punkt','stopwords','punkt_tab'], quiet=True)\nfrom nltk.tokenize import word_tokenize\nfrom nltk.corpus import stopwords\nimport google.generativeai as genai\nprint('Ready')"
   ],
   "outputs": [],
   "execution_count": null
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Text Preprocessing \u2014 Slogan Dataset"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Load slogan dataset\ntry:\n    df_slogans = pd.read_csv('/content/drive/MyDrive/BrandMind_Datasets/slogans.csv')\nexcept:\n    df_slogans = pd.DataFrame({'slogan': [\n        'Innovation for a better tomorrow',\n        'Quality you can trust, every time',\n        'Building the future, together',\n        'Excellence in every detail',\n        'Your success is our mission',\n    ] * 100, 'industry': ['Technology','Finance','Healthcare','Retail','Education'] * 100})\n\nstop_words = set(stopwords.words('english'))\n\ndef preprocess_slogan(text):\n    text = str(text).lower()\n    text = re.sub(r'[^\\w\\s]', '', text)       # Remove punctuation\n    text = re.sub(r'\\s+', ' ', text).strip()  # Normalise spaces\n    tokens = word_tokenize(text)\n    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]\n    return tokens\n\ndf_slogans['tokens'] = df_slogans['slogan'].apply(preprocess_slogan)\ndf_slogans['clean']  = df_slogans['tokens'].apply(lambda t: ' '.join(t))\ndf_slogans['word_count'] = df_slogans['slogan'].apply(lambda x: len(x.split()))\n\nprint(df_slogans[['slogan','clean','word_count']].head())"
   ],
   "outputs": [],
   "execution_count": null
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Slogan Generation via Gemini API"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Configure Gemini\nGEMINI_API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your key\ngenai.configure(api_key=GEMINI_API_KEY)\nmodel = genai.GenerativeModel('gemini-pro')\n\ndef generate_slogans(company, industry, tone, audience, n=5):\n    prompt = f\"\"\"You are a world-class brand copywriter.\nCompany: {company}\nIndustry: {industry}\nBrand Tone: {tone}\nTarget Audience: {audience}\n\nGenerate {n} unique, punchy, memorable slogans for this brand.\nEach should be max 8 words and capture the brand essence.\nReturn as JSON: {{\"slogans\": [{{\"text\": \"...\", \"vibe\": \"one-word description\"}}]}}\"\"\"\n    try:\n        response = model.generate_content(prompt)\n        data = json.loads(response.text.replace('```json','').replace('```','').strip())\n        return data['slogans']\n    except Exception as e:\n        print(f'API error: {e} \u2014 using fallback')\n        return [\n            {'text': f'{company} \u2014 Built for what\\'s next.', 'vibe': 'Forward-looking'},\n            {'text': f'Think different. Choose {company}.', 'vibe': 'Bold'},\n            {'text': f'{company}. Simply brilliant.', 'vibe': 'Minimalist'},\n            {'text': f'Where {industry} meets excellence.', 'vibe': 'Premium'},\n            {'text': f'The future of {industry} starts here.', 'vibe': 'Inspirational'},\n        ]\n\nslogans = generate_slogans('BrandMind', 'Technology', 'Innovative', 'Startup founders')\nfor s in slogans:\n    print(f\"  [{s['vibe']}] {s['text']}\")"
   ],
   "outputs": [],
   "execution_count": null
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Preliminary Multilingual Translation (W4 requirement)"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "def translate_slogan(slogan, target_lang):\n    prompt = f\"\"\"Translate this brand slogan to {target_lang}. Preserve tone and punchiness.\nSlogan: '{slogan}'\nReturn ONLY the translated text.\"\"\"\n    try:\n        return model.generate_content(prompt).text.strip()\n    except:\n        return f'[{target_lang} translation of: {slogan}]'\n\n# Preview multilingual (preliminary \u2014 full version in Week 8)\nselected_slogan = slogans[0]['text']\nprint(f'Original: {selected_slogan}\\n')\nfor lang in ['Spanish', 'French', 'German']:\n    translated = translate_slogan(selected_slogan, lang)\n    print(f'{lang}: {translated}')"
   ],
   "outputs": [],
   "execution_count": null
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "# Save slogans to file (downloadable)\nimport os\nos.makedirs('outputs', exist_ok=True)\nwith open('outputs/slogans.json', 'w') as f:\n    json.dump({'company': 'BrandMind', 'slogans': slogans}, f, indent=2)\nprint('Saved: outputs/slogans.json')\n\nslogan_txt = '\\n'.join([f\"{i+1}. [{s['vibe']}] {s['text']}\" for i, s in enumerate(slogans)])\nwith open('outputs/slogans.txt', 'w') as f:\n    f.write(slogan_txt)\nprint('Saved: outputs/slogans.txt')"
   ],
   "outputs": [],
   "execution_count": null
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Week 4 Complete \u2705\n- \u2705 NLTK preprocessing (tokenise, lowercase, remove punctuation)\n- \u2705 Gemini API slogan generation with persona input\n- \u2705 5 slogans per company\n- \u2705 Preliminary multilingual translation\n- \u2705 Downloadable slogan list (JSON + TXT)"
   ]
  }
 ]
}