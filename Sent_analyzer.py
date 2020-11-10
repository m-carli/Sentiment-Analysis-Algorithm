#UNIVERSAL SENTIMENT ANALYZER

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from matplotlib import pyplot
import sys
import os
from textblob import TextBlob

analyzer = SentimentIntensityAnalyzer()
#print("Hi, Mr. Analyzer here.")
book = input('Insert source book: ')
window_value = input('Insert window width: ')
choice = input('Go directly to graph? y/n ')

def create_graph(file, subj, win):
    #CREATE PANDAS DATASET FROM .TXT AND ROLLING
    data_book = pd.read_csv(file, sep="\n", header=None, index_col=None)
    data_subj = pd.read_csv(subj, sep="\n", header=None, index_col=None)

    print('data read successfully.')

    rolling = data_book.rolling(window=int(win))
    rolling_mean = rolling.mean()
    rolling_s = data_subj.rolling(window=int(win))
    rolling_subj = rolling_s.mean()

    #PLOT DATA
    print('Making sentiment graph...')
    rolling_mean.plot(title='Sentiment tendency')
    pyplot.show()
    print('Making subjectivity graph...')
    rolling_subj.plot(color='green', title='Subjectivity tendency')
    pyplot.show()

if choice == 'n':
    #ESTRARRE POLARITA' E CREARE DATASET
    try:
        os.mkdir('Novels data')
    except: #Exception as e:
        pass
    try:
        os.mkdir(f'Novels data\Catalogues {book}')
    except:
        pass
    
    parameter = input('Insert compound threshold for registration: ')
    polarities = []
    positive_sent = {}
    negative_sent = {}
    all_sentences = []
    subjectivity = {}
    high_subj = {}
    
    index = 0
    try:
        with open(f"Novels/{book}.txt","r",encoding="utf-8") as f:
            for sentence in f.read().split('.'):
                index += 1
                all_sentences.append(sentence)
                vs = analyzer.polarity_scores(sentence)
                polarities.append(vs['compound'])
                if vs['compound'] >= float(parameter):
                    positive_sent.update({index:vs['compound']})
                elif vs['compound'] <= -float(parameter):
                    negative_sent.update({index:vs['compound']})

                analysis = TextBlob(sentence)
                subjectivity[index] = str(analysis.sentiment.subjectivity)
                if analysis.sentiment.subjectivity > 0.9:
                    high_subj[index] = str(analysis.sentiment.subjectivity)

            print('Number of sentences: ' + str(index) + '.\nTen percent: {}'.format(index/10))

    except Exception as e:
        sys.exit(e)

    len_pol = len(polarities)

    print(f'{book} data processed.')

    #CREATE FILE WITH NUMBERED SENTENCES
    index = 0
    with open(f"Novels data/Catalogues {book}/{book}_catalogue.txt","w") as file:
        for sentence in all_sentences:
            file.write(str(index) + ' > ' + sentence + '\n')
            index += 1

    print(f'{book} catalogue created')

    #CREATE FILE TO REGISTER POSITION OF PARTICULARLY LOW OR HIGH VALUES
    with open(f"Novels data/Catalogues {book}/{book}_sentences_positive.txt","w") as f:
        for element in positive_sent:
            f.write(str(element) + '> ' + str(positive_sent[element]) + '\n')
        f.close()

    with open(f"Novels data/Catalogues {book}/{book}_sentences_negative.txt","w") as f:
        for element in negative_sent:
            f.write(str(element) + '> ' + str(negative_sent[element]) + '\n')
        f.close()

    print(f'{book}_sentences created')

    names = []
    for n in range(0, len_pol):
        names.append(n)

    #DATASET FILE
    with open(f"Novels data/Catalogues {book}/data_{book}.txt","w") as f:
        for n in names:
            f.write(str(polarities[n]) + '\n')
        f.close()

    print(f'data_{book} created.')

    with open(f"Novels data/Catalogues {book}/{book}_subjectivity.txt","w") as f:
        for element in subjectivity:
            f.write(str(subjectivity[element]) + '\n')
        f.close()

    with open(f"Novels data/Catalogues {book}/{book}_subjectivity_index.txt","w") as f:
        for element in high_subj:
            f.write(str(element) + '> ' + str(subjectivity[element]) + '\n')
        f.close()

    print(f'{book}_subjectivity and subj index created')
    dir_sub = f"Novels data/Catalogues {book}/{book}_subjectivity.txt" 
    create_graph(f'Novels data/Catalogues {book}/data_{book}.txt', dir_sub, window_value)

else:
    try:
        dir_sub = f"Novels data/Catalogues {book}/{book}_subjectivity.txt" 
        create_graph(f'Novels data/Catalogues {book}/data_{book}.txt', dir_sub, window_value)
    except Exception as e:
        print(e)
        
