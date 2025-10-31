# 🪏 Bolongo
A chatbot to help with common questions about growing trees in Old School RuneScape, using natural language processing to provide accurate answers in a gnome-inspired tone.

**[Chat with Bolongo 💬](https://bolongo.streamlit.app/)**

![Title](/title.png)

### 🌱 Features

- **Patches:** Discover the location of every tree patch in Gielinor
  - *"Give me a list of all regular tree patches."*
- **Transportation:** Get detailed directions and transportation methods for each patch
  - *"Where is the Catherby patch?"*
- **Requirements:** Search level requirements for any tree, and quest requirements for specific patches
  - *"What Farming level do I need to plant Maple trees?"*
  - *"What are the requirements for the Nemus Retreat patch?"*
- **Recommendations:** Learn the best trees to plant based on your Farming level
  - *"Which trees should I grow at level 27?"*
- **Duration:** See how long specific trees take to grow
  - *"How long do Willow trees take to grow?"*
- **Protection:** Check the correct protection payment for each tree
  - *"What do I give to the gardener to protect Yew trees?"*


### ⚙️ Tech Stack

- **Frontend:** Streamlit
- **NLP:** scikit-learn (Logistic Regression classifier with TF-IDF vectorisation)
- **Data Processing:** pandas
- **Language:** Python 3

### 🤖 How It Works

1. **User Input:** You ask a question
2. **Intent Classification**: A trained machine learning model identifies your intent
3. **Data Retrieval**: The system queries relevant data from CSV files
4. **Response Generation**: A natural-sounding response is generated using templates

### 📁 Project Structure

```
Bolongo/
├── bolongo.py              # Main Streamlit application
├── assets/                 # Images and fonts
│   ├── bolongo_chathead.png
│   ├── bolongo_standing.png
│   ├── grand_tree.png
│   ├── RuneScape-Bold-12.ttf
│   └── RuneScape-Plain-12.ttf
├── config/                 # Configuration files
│   ├── intent_mapping.py   
│   └── response_bank.md    
├── data/                   # CSV data files
│   ├── trees_df.csv
│   └── patches_df.csv
├── models/                 # Trained ML models
│   ├── classifier.pkl
│   └── vectoriser.pkl
├── source/                 # Core application logic
│   ├── answer_retriever.py
│   ├── intent_classifier.py
│   ├── orchestrator.py
│   └── response_generator.py
└── training/               # Model training scripts
    ├── question_bank.md
    ├── train_classifier_model.py
    └── training_data_generator.py
```

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- **[Old School RuneScape Wiki](https://oldschool.runescape.wiki/)** for the game data and images
- **[RuneStar](https://github.com/RuneStar)** for the fonts

---

*This project is a fan-made tool and is not affiliated with or endorsed by Jagex Ltd. Old School RuneScape is a registered trademark of Jagex Ltd.*
