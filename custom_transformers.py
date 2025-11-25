# import numpy as np
# from sklearn.base import TransformerMixin, BaseEstimator
# from sklearn.decomposition import TruncatedSVD
# from transformers import (
#     DistilBertForSequenceClassification,
#     DistilBertTokenizer,
#     RobertaForSequenceClassification,
#     RobertaTokenizer,
#     BertForSequenceClassification,
#     BertTokenizer,
# )
# import torch
# from pathlib import Path
# import os

# # Custom Transformer to calculate and retain 98% variance for TruncatedSVD
# class OptimalSVD(TransformerMixin):
#     def __init__(self, variance_threshold=0.98, random_state=42):
#         self.variance_threshold = variance_threshold
#         self.random_state = random_state
#         self.svd = None
#         self.n_components_ = None

#     def fit(self, X, y=None):
#         # Initial SVD to compute explained variance
#         svd = TruncatedSVD(n_components=X.shape[1] - 1, random_state=self.random_state)
#         svd.fit(X)
#         cumulative_variance = np.cumsum(svd.explained_variance_ratio_)
#         self.n_components_ = np.argmax(cumulative_variance >= self.variance_threshold) + 1
#         print(f"-> Optimal number of components for {self.variance_threshold * 100:.0f}% variance: {self.n_components_}")
        
#         # Fit SVD with optimal components
#         self.svd = TruncatedSVD(n_components=self.n_components_, random_state=self.random_state)
#         self.svd.fit(X)
#         return self

#     def transform(self, X):
#         # Transform data using the fitted SVD
#         return self.svd.transform(X)

#     def fit_transform(self, X, y=None):
#         self.fit(X, y)
#         return self.transform(X)

# # Binary-to-Multiclass Pipeline
# class BinaryToMulticlassPipeline(BaseEstimator, TransformerMixin):
#     def __init__(self, binary_model=None, multiclass_model=None):
#         self.binary_model = binary_model
#         self.multiclass_model = multiclass_model

#     def fit(self, X, y):
#         print(f"-> Fitting Model")
#         # Map labels for binary classification: NP (2) -> 0, P (0 or 1) -> 1
#         y_binary = np.where(y == 2, 0, 1)  # 0 -> NP, 1 -> P
        
#         # Train binary model to classify NP vs P
#         self.binary_model.fit(X, y_binary)

#         # Filter samples classified as 'P' and train the multiclass model
#         X_p = X[y_binary == 1]
#         y_p = y[y_binary == 1]  # Keep original labels for PFR (0) and PB (1)
#         self.multiclass_model.fit(X_p, y_p)
#         return self

#     def predict(self, X):
#         # Predict binary labels: NP vs P
#         y_binary_pred = self.binary_model.predict(X)

#         # Initialize predictions with binary results
#         y_pred = np.full_like(y_binary_pred, 2)  # Default to NP (2)

#         # For samples classified as 'P', use the multiclass model
#         X_p = X[y_binary_pred == 1]
#         if len(X_p) > 0:
#             y_p_pred = self.multiclass_model.predict(X_p)
#             y_pred[y_binary_pred == 1] = y_p_pred

#         return y_pred

#     def decision_function(self, X):
#         # Get decision function scores for binary model
#         binary_decision = self.binary_model.decision_function(X).ravel()
        
#         # Initialize decision scores for 3 classes
#         multiclass_scores = np.zeros((X.shape[0], 3))  # 3 classes: PFR (0), PB (1), NP (2)
        
#         # Map binary decision scores
#         multiclass_scores[:, 2] = -binary_decision  # NP class scores (negative of decision score)
#         multiclass_scores[:, :2] = np.column_stack((binary_decision, binary_decision))  # Duplicate scores for PFR and PB

#         # Further split P into PFR and PB using the multiclass model
#         p_indices = binary_decision > 0  # Binary threshold: >0 means classified as P
#         X_p = X[p_indices]
#         if len(X_p) > 0:
#             p_decision = self.multiclass_model.decision_function(X_p)
#             if len(p_decision.shape) == 1:  # Ensure p_decision is 2D
#                 p_decision = np.column_stack((p_decision, -p_decision))
#             multiclass_scores[p_indices, :2] = p_decision

#         return multiclass_scores

#     def predict_proba(self, X):
#         # Combine probabilities for P/NP and PFR/PB
#         binary_probs = self.binary_model.predict_proba(X)
#         multiclass_probs = np.zeros((X.shape[0], 3))  # 3 classes: PFR (0), PB (1), NP (2)

#         # Map binary probabilities (P/NP)
#         multiclass_probs[:, 2] = binary_probs[:, 0]  # NP probabilities
#         p_indices = np.argmax(binary_probs, axis=1) == 1  # Samples classified as P
#         X_p = X[p_indices]

#         if len(X_p) > 0:
#             p_probs = self.multiclass_model.predict_proba(X_p)
#             multiclass_probs[p_indices, :2] = p_probs

#         return multiclass_probs

# # Word2Vec Transformer
# class Word2VecTransformer(BaseEstimator, TransformerMixin):
#     def __init__(self, model):
#         self.model = model
#         self.vector_size = model.vector_size

#     def transform(self, X, **transform_params):
#         """Transform documents to their Word2Vec embeddings."""
#         return np.array([self._document_vector(doc) for doc in X])

#     def fit(self, X, y=None, **fit_params):
#         return self

#     def _document_vector(self, doc):
#         """Compute the document vector as the average of word vectors."""
#         tokens = doc.split()  # Tokenize the document
#         vectors = [self.model.wv[word] for word in tokens if word in self.model.wv]
#         if vectors:
#             return np.mean(vectors, axis=0)
#         else:
#             return np.zeros(self.vector_size)

# # Identity Transform
# def identity_transform(x):
#     return x

# # BERT Inference Loader
# def bert_class_inference(model_name, model_path):
#     model = None
#     tokenizer = None
#     max_length = 128
#     batch_size = 8
    
#     if 'distilbert' in model_name:
#         model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=3)
#         tokenizer = DistilBertTokenizer.from_pretrained(model_name)
#     elif 'roberta' in model_name:
#         model = RobertaForSequenceClassification.from_pretrained(model_name, num_labels=3)
#         tokenizer = RobertaTokenizer.from_pretrained(model_name)
#     elif 'bert' in model_name:
#         model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)
#         tokenizer = BertTokenizer.from_pretrained(model_name)
#     else:
#         raise ValueError(f"Unsupported model name: {model_name}")
        
#     model.load_state_dict(torch.load(model_path, weights_only=True))
#     model.eval()
#     return model, tokenizer, max_length
import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.decomposition import TruncatedSVD

# NOTE:
# We removed heavy dependencies like torch and transformers
# to make this module lightweight and safe to import everywhere.


# -----------------------------
# OptimalSVD
# -----------------------------
class OptimalSVD(TransformerMixin):
    def __init__(self, variance_threshold=0.98, random_state=42):
        self.variance_threshold = variance_threshold
        self.random_state = random_state
        self.svd = None
        self.n_components_ = None

    def fit(self, X, y=None):
        # Initial SVD to compute explained variance
        svd = TruncatedSVD(
            n_components=X.shape[1] - 1,
            random_state=self.random_state
        )
        svd.fit(X)
        cumulative_variance = np.cumsum(svd.explained_variance_ratio_)
        self.n_components_ = np.argmax(
            cumulative_variance >= self.variance_threshold
        ) + 1
        print(
            f"-> Optimal number of components for "
            f"{self.variance_threshold * 100:.0f}% variance: "
            f"{self.n_components_}"
        )

        # Fit SVD with optimal components
        self.svd = TruncatedSVD(
            n_components=self.n_components_,
            random_state=self.random_state
        )
        self.svd.fit(X)
        return self

    def transform(self, X):
        return self.svd.transform(X)

    def fit_transform(self, X, y=None):
        self.fit(X, y)
        return self.transform(X)


# -----------------------------
# BinaryToMulticlassPipeline
# -----------------------------
class BinaryToMulticlassPipeline(BaseEstimator, TransformerMixin):
    def __init__(self, binary_model=None, multiclass_model=None):
        self.binary_model = binary_model
        self.multiclass_model = multiclass_model

    def fit(self, X, y):
        print("-> Fitting Model")
        # Map labels for binary classification: NP (2) -> 0, P (0 or 1) -> 1
        y_binary = np.where(y == 2, 0, 1)  # 0 -> NP, 1 -> P

        # Train binary model to classify NP vs P
        self.binary_model.fit(X, y_binary)

        # Filter samples classified as 'P' and train the multiclass model
        X_p = X[y_binary == 1]
        y_p = y[y_binary == 1]  # labels for PFR (0) and PB (1)
        self.multiclass_model.fit(X_p, y_p)
        return self

    def predict(self, X):
        # Predict binary labels: NP vs P
        y_binary_pred = self.binary_model.predict(X)

        # Initialize predictions with NP (2)
        y_pred = np.full_like(y_binary_pred, 2)

        # For samples classified as 'P', use the multiclass model
        X_p = X[y_binary_pred == 1]
        if len(X_p) > 0:
            y_p_pred = self.multiclass_model.predict(X_p)
            y_pred[y_binary_pred == 1] = y_p_pred

        return y_pred

    def decision_function(self, X):
        binary_decision = self.binary_model.decision_function(X).ravel()
        multiclass_scores = np.zeros((X.shape[0], 3))  # PFR (0), PB (1), NP (2)

        multiclass_scores[:, 2] = -binary_decision
        multiclass_scores[:, :2] = np.column_stack(
            (binary_decision, binary_decision)
        )

        p_indices = binary_decision > 0
        X_p = X[p_indices]
        if len(X_p) > 0:
            p_decision = self.multiclass_model.decision_function(X_p)
            if len(p_decision.shape) == 1:
                p_decision = np.column_stack((p_decision, -p_decision))
            multiclass_scores[p_indices, :2] = p_decision

        return multiclass_scores

    def predict_proba(self, X):
        binary_probs = self.binary_model.predict_proba(X)
        multiclass_probs = np.zeros((X.shape[0], 3))  # PFR (0), PB (1), NP (2)

        multiclass_probs[:, 2] = binary_probs[:, 0]  # NP
        p_indices = np.argmax(binary_probs, axis=1) == 1
        X_p = X[p_indices]

        if len(X_p) > 0:
            p_probs = self.multiclass_model.predict_proba(X_p)
            multiclass_probs[p_indices, :2] = p_probs

        return multiclass_probs


# -----------------------------
# Word2VecTransformer
# -----------------------------
class Word2VecTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model):
        self.model = model
        self.vector_size = model.vector_size

    def transform(self, X, **transform_params):
        return np.array([self._document_vector(doc) for doc in X])

    def fit(self, X, y=None, **fit_params):
        return self

    def _document_vector(self, doc):
        tokens = doc.split()
        vectors = [self.model.wv[word] for word in tokens if word in self.model.wv]
        if vectors:
            return np.mean(vectors, axis=0)
        return np.zeros(self.vector_size)


# -----------------------------
# Identity transform
# -----------------------------
def identity_transform(x):
    return x


# -----------------------------
# Optional stub for BERT
# -----------------------------
def bert_class_inference(*args, **kwargs):
    """
    Stubbed out: original implementation required torch + transformers.
    Kept only so imports won't break. Not used in current deployment.
    """
    raise NotImplementedError(
        "BERT inference is disabled in this environment (no torch backend)."
    )
