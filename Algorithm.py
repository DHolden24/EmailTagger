from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


def create_pipeline(ngram_range, max_df, min_df, use_idf, smooth_idf, sublinear_tf, alpha, fit_prior):
    """ Create a pipeline with the given arguments and return it """
    return Pipeline([('vectorizer', CountVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df)),
                    ('transformer', TfidfTransformer(use_idf=use_idf, smooth_idf=smooth_idf, sublinear_tf=sublinear_tf)),
                    ('classifier', MultinomialNB(alpha=alpha, fit_prior=fit_prior)),])


def train(pipeline, train_data, train_target, test_data=None, test_target=None):
    """ Take the given pipeline and train it on the given data, testing it as well if test data provided 
    
    Key Word Arguments
    pipeline -- The pipeline to be trained
    train_data -- The data to train on
    train_target -- The expected output for the training data
    test_data -- The data to test with
    test_target -- The expected output for the test data
    """
    pipeline = pipeline.fit(train_data, train_target)

    if not test_data and test_target:
        return pipeline

    predicted_tags = pipeline.predict(test_data)
    import numpy as np
    print(np.mean(predicted_tags == test_target))

    return pipeline


def tune_classifier(pipeline, train_data, train_target):
    """ Tune the given classifier using the given data """
    from sklearn.model_selection import GridSearchCV

    # Initialize the list of parameters
    parameters = {'vectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
                  'vectorizer__max_df': [0.5, 0.65, 0.75, 0.85, 1.0],
                  'vectorizer__min_df': [0.0, 0.15, 0.25, 0.45],
                  'transformer__use_idf': (True, False),
                  'transformer__smooth_idf': (True, False),
                  'transformer__sublinear_tf': (True, False),
                  'classifier__alpha': (1e-2, 1e-3),
                  'classifier__fit_prior': (True, False),}
    
    # Tune the pipeline using a grid search
    print("tuning")
    tuner = GridSearchCV(pipeline, parameters, n_jobs=1)
    tuner = tuner.fit(train_data, train_target)

    # Write the results to a txt file
    file = open("TuningResults.txt", 'a+')
    file.write("Best Score: " + str(tuner.best_score_))
    file.write("\n")
    file.write("Best Parameters:\n")
    file.write(str(tuner.best_params_))
    file.write("\n\n\n")
    file.close()
