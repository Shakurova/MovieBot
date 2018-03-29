# re-save pretrained GloVe in word2vec format
from gensim.scripts.glove2word2vec import glove2word2vec
glove_input_file = 'D:\Data\word2vec\glove.6B.100d.txt'
word2vec_output_file = 'D:\Data\word2vec\glove.6B.100d.txt.word2vec'
glove2word2vec(glove_input_file, word2vec_output_file)