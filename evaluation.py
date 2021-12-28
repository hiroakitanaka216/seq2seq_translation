# this program was referred from https://pytorch.org/tutorials/intermediate/seq2seq_translation_tutorial.html
# dataset was referred from https://www.manythings.org/anki/

from __future__ import unicode_literals, print_function, division
import random
import torch
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import argparse
import os
import re


import lang_data
import seq2seq_GRU
import seq2seq_RNN
import train

parser = argparse.ArgumentParser()
parser.add_argument('--epoch', type=int, default=75000) #or default=1
args = parser.parse_args()

def evaluate(encoder, decoder, sentence, max_length=lang_data.MAX_LENGTH):
    with torch.no_grad():
        input_tensor = seq2seq_RNN.tensorFromSentence(lang_data.input_lang, sentence) #model
        input_length = input_tensor.size()[0]
        encoder_hidden = encoder.initHidden()

        encoder_outputs = torch.zeros(max_length, encoder.hidden_size, device=seq2seq_RNN.device) #model

        for ei in range(input_length):
            encoder_output, encoder_hidden = encoder(input_tensor[ei],
                                                     encoder_hidden)
            encoder_outputs[ei] += encoder_output[0, 0]

        decoder_input = torch.tensor([[lang_data.SOS_token]], device=seq2seq_RNN.device)  # SOS #model

        decoder_hidden = encoder_hidden

        decoded_words = []
        decoder_attentions = torch.zeros(max_length, max_length)

        for di in range(max_length):
            decoder_output, decoder_hidden, decoder_attention = decoder(
                decoder_input, decoder_hidden, encoder_outputs)
            decoder_attentions[di] = decoder_attention.data
            topv, topi = decoder_output.data.topk(1)
            if topi.item() == lang_data.EOS_token:
                decoded_words.append('<EOS>')
                break
            else:
                decoded_words.append(lang_data.output_lang.index2word[topi.item()])

            decoder_input = topi.squeeze().detach()

        return decoded_words, decoder_attentions[:di + 1]


######################################################################
# We can evaluate random sentences from the training set and print out the
# input, target, and output to make some subjective quality judgements:
#

def evaluateRandomly(encoder, decoder, n=10):
    print('>:input, =:target, <:output')
    for i in range(n):
        pair = random.choice(lang_data.pairs)
        print('>', pair[0])
        print('=', pair[1])
        output_words, attentions = evaluate(encoder, decoder, pair[0])
        output_sentence = ' '.join(output_words)
        print('<', output_sentence)
        print('')


######################################################################
# Training and Evaluating
# =======================
#
# With all these helper functions in place (it looks like extra work, but
# it makes it easier to run multiple experiments) we can actually
# initialize a network and start training.
#
# Remember that the input sentences were heavily filtered. For this small
# dataset we can use relatively small networks of 256 hidden nodes and a
# single GRU layer. After about 40 minutes on a MacBook CPU we'll get some
# reasonable results.
#
# .. Note::
#    If you run this notebook you can train, interrupt the kernel,
#    evaluate, and continue training later. Comment out the lines where the
#    encoder and decoder are initialized and run ``trainIters`` again.
#

hidden_size = 256
encoder1 = seq2seq_RNN.EncoderRNN(lang_data.input_lang.n_words, hidden_size).to(seq2seq_RNN.device) #model
attn_decoder1 = seq2seq_RNN.AttnDecoderRNN(hidden_size, lang_data.output_lang.n_words, dropout_p=0.1).to(seq2seq_RNN.device) #model

train.trainIters(encoder1, attn_decoder1, args.epoch, print_every=5000)

######################################################################
#

evaluateRandomly(encoder1, attn_decoder1)


######################################################################
# Visualizing Attention
# ---------------------
#
# A useful property of the attention mechanism is its highly interpretable
# outputs. Because it is used to weight specific encoder outputs of the
# input sequence, we can imagine looking where the network is focused most
# at each time step.
#
# You could simply run ``plt.matshow(attentions)`` to see attention output
# displayed as a matrix, with the columns being input steps and rows being
# output steps:
#

output_words, attentions = evaluate(encoder1, attn_decoder1, "je suis trop froid .")

#output_words, attentions = evaluate(encoder1, attn_decoder1, "空気 が 暖かく なっ た 。")

plt.matshow(attentions.numpy())


######################################################################
# For a better viewing experience we will do the extra work of adding axes
# and labels:
#

def showAttention(input_sentence, output_words, attentions):
    # Set up figure with colorbar
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(attentions.numpy(), cmap='bone', vmin=0, vmax=1)
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + input_sentence.split(' ') +
                       ['<EOS>'], rotation=90)
    ax.set_yticklabels([''] + output_words)

    # Show label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    plt.show()

    rstrip_sentence = input_sentence.rstrip('?')
    dir_name = f'results/attention_image'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    fig.savefig(f"{dir_name}/{rstrip_sentence.replace(' ', '_')}.png")

line_eng = []

def evaluateAndShowAttention(input_sentence):
    output_words, attentions = evaluate(
        encoder1, attn_decoder1, input_sentence)
    print('input =', input_sentence)
    print('output =', ' '.join(output_words))
    line_eng.append(' '.join(output_words))
    ff = open('data/for_evaluation/eng-fra_output_pred(eng).txt', 'w', encoding="utf-8")
    ff.writelines([w + '\n' for w in line_eng])
    ff.close()
    showAttention(input_sentence, output_words, attentions)

f0 = open("data/for_evaluation/eng-fra_input(fra).txt","r", encoding="utf-8")
line_fr0 = f0.readlines()
line_fr = []

for x in line_fr0:
    line_fr.append(x.replace("\n", ""))

for i in range(0, len(line_fr)):
  s = str(line_fr[i])
  evaluateAndShowAttention(s)

'''
#eng-fra 4 examples version
evaluateAndShowAttention("elle a cinq ans de moins que moi .")

evaluateAndShowAttention("elle est trop petit .")

evaluateAndShowAttention("je ne crains pas de mourir .")

evaluateAndShowAttention("c est un jeune directeur plein de talent .")
'''
