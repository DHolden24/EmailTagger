import win32com.client
import Algorithm
import Cleaner
import os
import pickle
import time

pipeline_save_file = "TaggerSave/Tagger"
email = "INSERT_EMAIL_HERE"

if __name__ == "__main__":
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.Folders(email).Folders("Inbox")

    if os.path.isfile(pipeline_save_file):
        file = open(pipeline_save_file, 'rb')
        pipeline, tags = pickle.load(file)
        file.close()

    else:
        pipeline = Algorithm.create_pipeline(ngram_range=(1, 3), max_df=0.65, min_df=0.0,
                                             use_idf=False, smooth_idf=True, sublinear_tf=False,
                                             alpha=0.01, fit_prior=True)

        training_docs, training_tags = [], []
        testing_docs, testing_tags = [], []
        count = 0
        for item in inbox.Items:
            if item.Categories != "":
                #training_docs.append(Cleaner.clean_string(item.Body))
                #training_tags.append(item.Categories)
                if count % 5 != 0:
                    training_docs.append(Cleaner.clean_string(item.Body))
                    training_tags.append(item.Categories)
                else:
                    testing_docs.append(Cleaner.clean_string(item.Body))
                    testing_tags.append(item.Categories)
                count += 1

        tags = list(set(training_tags + testing_tags))
        for i in range(len(training_tags)):
            training_tags[i] = tags.index(training_tags[i])
        for i in range(len(testing_tags)):
            testing_tags[i] = tags.index(testing_tags[i])

        # Algorithm.tune_classifier(pipeline, training_docs, training_tags)

        pipeline = Algorithm.train(pipeline=pipeline, train_data=training_docs, train_target=training_tags,
                                   test_data=testing_docs, test_target=testing_tags)

        file = open(pipeline_save_file, 'ab')
        pickle.dump((pipeline, tags), file)
        file.close()

    latest_item = inbox.Items.GetLast()
    print("Ready")
    while True:
        item = inbox.Items.GetLast()

        if item.Subject != latest_item.Subject or item.Body != latest_item.Body:
            tag = tags[pipeline.predict([Cleaner.clean_string(item.Body)])[0]]

            item.Categories = tag
            item.Save()

            latest_item = item

        time.sleep(5)

    pass

