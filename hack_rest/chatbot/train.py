import pandas as pd
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)


def train_classification_ai_model():
    # Load and prepare the dataset
    # This is a placeholder. Replace with your actual dataset loading logic.
    # For example, you can load from a CSV file or any other source.

    df = pd.read_excel("./hack_rest/nlp_pipeline/training_data/Hackathon_business.xlsx")

    # Encode labels
    le = LabelEncoder()
    # df['label_id'] = le.fit_transform(df['label'])
    df["business_category_id"] = le.fit_transform(df["Business Category"])

    # Tokenize text
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    def tokenize(batch):
        return tokenizer(batch["Sentances or word"], padding=True, truncation=True)

    dataset = Dataset.from_pandas(df[["Sentances or word", "business_category_id"]])
    dataset = dataset.map(tokenize, batched=True)
    dataset = dataset.rename_column("business_category_id", "label")
    dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=len(le.classes_)
    )

    training_args = TrainingArguments(
        output_dir="./hack_rest/chatbot/business_classifier/results",
        num_train_epochs=5,
        per_device_train_batch_size=4,
        logging_dir="./hack_rest/chatbot/business_classifier/logs",
        logging_steps=10,
        eval_strategy="no",
    )

    trainer = Trainer(model=model, args=training_args, train_dataset=dataset)

    trainer.train()

    model.save_pretrained("./hack_rest/chatbot/business_classifier")
    tokenizer.save_pretrained("./hack_rest/chatbot/business_classifier")
