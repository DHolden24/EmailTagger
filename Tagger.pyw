import win32com.client
import Algorithm
import Cleaner
import os
import pickle
import time

pipeline_save_file = "TaggerSave/Tagger"
email = "ENTER_EMAIL_HERE"
test_flag = False
tune_flag = False
classify_old = True

if __name__ == "__main__":
    # Open an outlook instance and the inbox
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders(email).Folders("Inbox")

    # If a previously created pipeline is saved, load it
    if os.path.isfile(pipeline_save_file):
        file = open(pipeline_save_file, 'rb')
        pipeline, tags = pickle.load(file)
        file.close()

    # Create a pipeline if none was found
    else:
        # These parameters were found using tuning
        pipeline = Algorithm.create_pipeline(ngram_range=(1, 3), max_df=0.65, min_df=0.0,
                                             use_idf=True, smooth_idf=True, sublinear_tf=False,
                                             alpha=0.01, fit_prior=True)

        # Initialize lists for the sets
        training_docs, training_tags = [], []
        testing_docs, testing_tags = [], []
        count = 0

        # For each tagged email in the inbox
        for item in inbox.Items:
            if item.Categories != "":

                # If the algorithm is being tested, take 20% of the tagged emails and use them as a test set
                if test_flag and count % 5 == 0:
                    testing_docs.append(Cleaner.clean_string(item.Body))
                    testing_tags.append(item.Categories)
                else:
                    training_docs.append(Cleaner.clean_string(item.Body))
                    training_tags.append(item.Categories)
                count += 1

        # Get the set of tags
        tags = list(set(training_tags + testing_tags))

        # Convert the tags in the training/testing lists to the index in the tag set
        for i in range(len(training_tags)):
            training_tags[i] = tags.index(training_tags[i])
        if test_flag:
            for i in range(len(testing_tags)):
                testing_tags[i] = tags.index(testing_tags[i])

        # Tune the classifier if indicated
        if tune_flag:
            Algorithm.tune_classifier(pipeline, training_docs, training_tags)

        # Train the pipeline
        pipeline = Algorithm.train(pipeline=pipeline, train_data=training_docs, train_target=training_tags,
                                   test_data=testing_docs if test_flag else None,
                                   test_target=testing_tags if test_flag else None)

        # Save the pipeline
        file = open(pipeline_save_file, 'ab')
        pickle.dump((pipeline, tags), file)
        file.close()

    # If we want to classify old emails
    if classify_old:
        for item in inbox.Items:
            if item.Categories == "":
                # Tag it and save it
                tag = tags[pipeline.predict([Cleaner.clean_string(item.Body)])[0]]
                item.Categories = tag
                item.Save()

    # Get the latest item
    latest_item = inbox.Items.GetLast()
    
    while True:
        item = inbox.Items.GetLast()

        # If a new email is received
        if item.Subject != latest_item.Subject or item.Body != latest_item.Body:
            # Tag it and save ite
            tag = tags[pipeline.predict([Cleaner.clean_string(item.Body)])[0]]
            item.Categories = tag
            item.Save()

            # The new item is the latest item
            latest_item = item

        # Sleep to reduce overhead of running this
        time.sleep(5)

    pass

