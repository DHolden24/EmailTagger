from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def create_pipeline(ngram_range, max_df, min_df, use_idf, smooth_idf, sublinear_tf, alpha, fit_prior):
    return Pipeline([('vectorizer', CountVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df)),
                    ('transformer', TfidfTransformer(use_idf=use_idf, smooth_idf=smooth_idf, sublinear_tf=sublinear_tf)),
                    ('classifier', MultinomialNB(alpha=alpha, fit_prior=fit_prior)),])


def train(pipeline, train_data, train_target, test_data=None, test_target=None):
    pipeline = pipeline.fit(train_data, train_target)

    if not test_data and test_target:
        return pipeline

    predicted_tags = pipeline.predict(test_data)
    import numpy as np
    print(np.mean(predicted_tags == test_target))

    return pipeline


def tune_classifier(pipeline, train_data, train_target):
    from sklearn.model_selection import GridSearchCV

    parameters = {'vectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
                  'vectorizer__max_df': [0.5, 0.65, 0.75, 0.85, 1.0],
                  'vectorizer__min_df': [0.0, 0.15, 0.25, 0.45],
                  'transformer__use_idf': (True, False),
                  'transformer__smooth_idf': (True, False),
                  'transformer__sublinear_tf': (True, False),
                  'classifier__alpha': (1e-2, 1e-3),
                  'classifier__fit_prior': (True, False),}
    print("tuning")
    tuner = GridSearchCV(pipeline, parameters, n_jobs=1)
    tuner = tuner.fit(train_data, train_target)

    file = open("TuningResults.txt", 'a+')
    file.write(str(tuner.best_score_))
    file.write("\n")
    file.write(str(tuner.best_params_))
    file.write("\n\n\n")
    file.close()
