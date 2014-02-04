# coding=utf-8

import Image, ImageDraw, ImageFont
import sys
import gflags

gflags.DEFINE_integer("draw_alignment_margin", 60, "the margin for alignment graph")
gflags.DEFINE_integer("draw_space_between_rows", 200, "the space between rows")
gflags.DEFINE_integer("draw_font_size", 40, "font size")
gflags.DEFINE_string("text_font", "simkai.ttf", "text font")

gflags.DEFINE_string('src_sentences', 'test/Eng.txt', 'the file containing source sentences. One sentence per line. Words are separated by spaces.')
gflags.DEFINE_string('trg_sentences', 'test/Chs.txt', 'the file containing translations of the source sentences. One sentence per line. Words are separated by spaces.')
gflags.DEFINE_string('align_file', 'test/Align.txt', "the file containing the alignment between source sentences and their translations. Each sentence's alignment is on one separate line. Alignments follow the GIZA++ format.")
gflags.DEFINE_integer('sentence_id', 0, "index starts from 0")
gflags.DEFINE_string('output_image', "output.png", "the output image")

def GetBoxes(words, (startx, starty), font):
    boxes = []
    first_word = True

    x = startx
    
    for word in words:
        if not first_word:
            x += font.getsize(' ')[0]
        word_x, word_y = font.getsize(word)
        boxes.append((x, starty, x + word_x, starty + word_y))
        x += word_x
        first_word = False

    return (boxes, (startx, starty, max(c for a, b, c, d in boxes), max(d for a, b, c, d in boxes)))

def DrawDirAlignToFile(sent1, sent2, align, filename):
    font = ImageFont.truetype(gflags.FLAGS.text_font, gflags.FLAGS.draw_font_size,
                              encoding = 'unic')
    make_unicode = lambda w: unicode(w)

    sent1 = map(make_unicode, sent1.split())
    sent2 = map(make_unicode, sent2.split())

    margin_size = gflags.FLAGS.draw_alignment_margin
    space_size = gflags.FLAGS.draw_space_between_rows
    word_boxes_1, (x1, y1, x2, y2) = GetBoxes(sent1, (margin_size, margin_size), font)
    word_boxes_2, (x1, y1, x2, y2) = GetBoxes(sent2, (x1, y2 + space_size), font)

    all_word_boxes = word_boxes_1 + word_boxes_2
    canvas_size = (max(x2 for x1, y1, x2, y2 in all_word_boxes) + margin_size * 2,
                   max(y2 for x1, y1, x2, y2 in all_word_boxes) + margin_size * 2)
    im = Image.new("RGB", canvas_size)

    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, canvas_size[0], canvas_size[1]), fill = 'WHITE')

    for word, (x1, y1, x2, y2) in zip(
        sent1 + sent2, word_boxes_1 + word_boxes_2):
        draw.rectangle((x1 - 1, y1 - 1, x2 + 1, y2 + 1), outline = 'GREY')
        draw.text((x1, y1), word, font = font, fill = "BLACK")

    for align_from, align_to in align:
        line_start_x = (word_boxes_1[align_from][0] + word_boxes_1[align_from][2]) / 2
        line_start_y = word_boxes_1[align_from][3]

        line_end_x = (word_boxes_2[align_to][0] + word_boxes_2[align_to][2]) / 2
        line_end_y = word_boxes_2[align_to][1]

        draw.line((line_start_x, line_start_y, line_end_x, line_end_y), fill="GREEN", width=2)

    del draw

    with open(filename, 'w') as ofile:
        im.save(ofile, "PNG")

def DrawDirAlignmentOfSentenceById(
    src_file, trg_file, align_file, sent_id, outputfile):
    # id starts from 0
    def GetIthSent(i, fn):
        with open(fn) as f:
            for li, l in enumerate(f):
                if i == li:
                    return unicode(l.strip(), 'utf8')

    def GetAligns(s):
        return [map(int, tuple(a.split('-'))) for a in s.split()]

    orig_sent = GetIthSent(sent_id, src_file)
    rt_sent = GetIthSent(sent_id, trg_file)
    align = GetAligns(GetIthSent(sent_id, align_file))
    DrawDirAlignToFile(orig_sent, rt_sent, align, outputfile)

if __name__ == "__main__":
##    DrawDirAlignToFile("I like machine translation .", u"我 喜欢 机器翻译 。", [(0, 0), (1, 1), (2, 2), (3, 2), (4, 3)], "test.png")
    try:
        argv = gflags.FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\nUsage: %s ARGS\n%s' % (e, sys.argv[0], FLAGS)
        sys.exit(1)

    src_file = gflags.FLAGS.src_sentences
    trg_file = gflags.FLAGS.trg_sentences
    align_file = gflags.FLAGS.align_file
    sent_id = gflags.FLAGS.sentence_id
    output_image = gflags.FLAGS.output_image

    DrawDirAlignmentOfSentenceById(
        src_file, trg_file, align_file, sent_id, output_image)
