# श्रीमद्भगवद्गीता · Śrīmad Bhagavad Gītā

A LaTeX/Devanāgarī edition of the Bhagavad Gītā — the eighteen-chapter dialogue between
Kṛṣṇa and Arjuna embedded in the Bhīṣma Parva of the Mahābhārata — together with its
traditional recitation apparatus (nyāsa, māhātmyams), a word-by-word split of every verse,
and full verse/word indices. Part of the [StotraSamhita](https://github.com/stotrasamhita)
family of Sanskrit-text projects.

## What's here

| File | Contents |
|---|---|
| `gita.tex` | The **mūlam** — all 18 chapters (adhyāyas) of the Gītā, verse by verse. |
| `nyasa.tex` | The **nyāsa** — the preparatory ṛṣi/chandas/devatā invocation and the *karanyāsa*/*hṛdayādi-nyāsa* recited before beginning the text. |
| `mahatmyam.tex` | A short, customary **Gītā-māhātmyam** — a handful of verses in praise of the Gītā, recited as an opener/closer around the text. |
| `mahatmyam-padma-puranam.tex` | The longer, **chapter-by-chapter Māhātmyam of the Gītā from the Padma Purāṇa** — a separate verse (or short passage) extolling the fruit of reciting each of the 18 chapters individually. |
| `mahatmyam-varaha-puranam.tex` | The Gītā-māhātmyam as it appears in the **Varāha Purāṇa**, opening with dhyāna-ślokas to Varāha. |
| `gsa.tex` | **गीतार्थसङ्ग्रहः** (Gītārtha-saṅgraha) — the 32-verse summary traditionally ascribed to Yāmunācārya (Āḷavandār), which distills the teaching of each chapter into a single verse; it opens by saluting Yāmuna's lotus feet. |
| `words/` | The word-split apparatus and indices — see below. |
| `gita.jpg`, `gitabook_cover.pdf`/`.svg` | Cover art. |
| `frontmatter.tex`, `preamble.tex`, `preface.tex`, `shloka.sty` | Shared front matter, LaTeX preamble, the Sanskrit preface (see below), and the verse-typesetting macros. |
| `gitabook.tps` | A TeXnicCenter editor project file (not part of the build). |

### `words/` — the pada-cchheda apparatus and indices

| File | What it is |
|---|---|
| `gita-words.tex` | The full text again, this time split word-by-word (**padacchheda**) under each verse. |
| `gitabook-annotated.tex`/`.pdf` | The combined edition: mūlam and padacchheda typeset together, with each hyperlinked to the other (see "Features" below). |
| `gita-word-splits.csv` | The underlying word-split data (chapter, verse, and each word of the verse in its own column) that `gita-words.tex` is derived from. |
| `index_moola.tex`, `index_word.tex` | The generated **śloka index** (verse openings, alphabetically) and **word index** (every one of ~3,800 unique padas, alphabetically, with every verse it occurs in). |
| `generate_index.py` | Reads `../gita.tex` and `gita-words.tex` and writes `index_moola.tex`/`index_word.tex`. |
| `extract_unique_words.py`, `syllabify.py` | Supporting scripts used while building the word list/indices from the CSV (`gita-wordlist*.txt`/`.json` are their output). |
| `hypershloka.sty` | Verse macros extended with the cross-linking used by the annotated edition. |
| `gita-words-kindle-scribe.tex`/`.pdf` | A standalone Kindle Scribe-sized edition of just the word-split text. |

## Editions

| Source | Output | Notes |
|---|---|---|
| `gitabook.tex` | [`gitabook.pdf`](https://github.com/stotrasamhita/gita/blob/master/gitabook.pdf) | Default digital edition (twoside, ~A5, Sanskrit 2003 font). |
| `gitabook-kindle.tex` | [`gitabook-kindle.pdf`](https://github.com/stotrasamhita/gita/blob/master/gitabook-kindle.pdf) | Kindle-sized (144×192mm), Siddhānta font, includes the Varāha Purāṇa māhātmyam. |
| `gitabook-kindle-scribe.tex` | [`gitabook-kindle-scribe.pdf`](https://github.com/stotrasamhita/gita/blob/master/gitabook-kindle-scribe.pdf) | Larger page for the Kindle Scribe's screen. |
| `gitabook-print.tex` | [`gitabook-print.pdf`](https://github.com/stotrasamhita/gita/blob/master/gitabook-print.pdf) | Print-oriented margins, includes the Varāha Purāṇa māhātmyam. |
| `words/gitabook-annotated.tex` | [`words/gitabook-annotated.pdf`](https://github.com/stotrasamhita/gita/blob/master/words/gitabook-annotated.pdf) | The mūlam + padacchheda cross-linked edition. |

Each edition `\input`s `nyasa.tex`, then `gita.tex`, then `mahatmyam.tex` (and, in the kindle/print editions, `mahatmyam-varaha-puranam.tex` as well), and closes with `gsa.tex`.

## Building

The documents are written for **XeLaTeX** (`% !TeX program = XeLaTeX` at the top of each file), using `fontspec` for Devanāgarī. You will need a TeX distribution with XeLaTeX and the Devanāgarī fonts each edition calls for by name — **Sanskrit 2003**, **Adishila**, or **Siddhānta**, depending on the file (check its `\setmainfont` line). To build, for example:

```sh
xelatex gitabook.tex
xelatex gitabook.tex   # run twice for the table of contents / cross-references
```

## Features of this edition

As the colophon in `frontmatter.tex` describes, this edition is organised into five parts —
मूलम् (the root text), पदच्छेदः (word splits), पद्मपुराणान्तर्गत-गीता-माहात्म्यम् (the
chapter-wise Māhātmyam from the Padma Purāṇa), श्लोकानुक्रमणिका (verse index), and
पदानुक्रमणिका (word index) — with a few things worth calling out:

- **Bidirectional linking** — in the annotated edition, clicking a verse number in the mūlam jumps forward to its split in the padacchheda, and clicking it there jumps back.
- **Visual continuity** — the two are typeset in sync so this back-and-forth navigation feels seamless.
- **Verse index** in the style of certain Purāṇa editions from Nag Publishers: śloka-pādas listed alphabetically, each hyperlinked to its place in the mūlam.
- **Word index** — an alphabetical concordance of all ~3,800 unique padas across all 18 chapters, each with hyperlinks to every verse it appears in.
- Consistent hyphenation in the mūlam, and careful, old-text-style use of avagraha (ऽ) to mark elided *a*-kāras in dīrgha sandhi.

## The preface

`preface.tex` (in Sanskrit) opens with the traditional salutation to the guru-paramparā and to Kṛṣṇa, then reflects on why this particular text: unlike Rāma, whose own words are comparatively rare in the Rāmāyaṇa — even when he speaks, he defers, out of humility, to the sages around him — Kṛṣṇa in his avatāra speaks directly and repeatedly as *jagadguru*, and the Gītā is the Upaniṣad-like heart of that teaching within the Mahābhārata. It quotes Ādi Śaṅkara's own tribute to the Gītā from the *Bhaja Govindam* ("even a little study of the Bhagavad Gītā, a drop of Gaṅgā-water, worship of Murāri just once, leaves no reckoning to be made with Yama"), the three verses on the Gītā's greatness spoken later in the Mahābhārata's own Gītā-parva ("let the Gītā, well sung, be sung again — what need is there of other, lengthy śāstras, when it flowed of its own accord from the lotus mouth of Padmanābha..."), and Arjuna's own plea within the text — "speak again, for there is no satiety in hearing this nectar" (10.18) — as the reason one returns to it again and again. It notes the custom of Gītā-pārāyaṇa on the final three tithis of Vaiśākha and Kārtika (said to give the fruit of an aśvamedha) and on Mārgaśīrṣa-Śukla-Ekādaśī, observed as *Gītā-jayantī*. It closes by citing the Gītā's own last word on the matter — that one who studies this dialogue is, by that very study, worshipped through a *jñāna-yajña* (18.70) — before bowing at Kṛṣṇa's feet. It is dated Pauṣa-Śukla-Pūrṇimā (Viśvāvasu saṃvatsara), January 2, 2026, and signed at *Sarvajñātma-Pratiṣṭhānam*.

## Acknowledgements

From the colophon: gratitude to the volunteers who proofread the various texts, to resources on archive.org including Śaṅkara Bhāṣyam and the Gita Press padaccheda, and especially to [Arindam Saha](https://github.com/arindamsaha1507/Gita/) for a high-quality CSV of pada splits (subsequently corrected and improved here). The core śloka-typesetting macros are credited to H. L. Prasād. The verse/word indices were generated with a custom Python pipeline (`words/generate_index.py` and friends).

## Usage

No separate LICENSE file is included in this repository; see the colophon in `frontmatter.tex` for the author's stated terms, and the [StotraSamhita](https://github.com/stotrasamhita) organization for related projects and [stotrasamhita.net](https://stotrasamhita.net).

---

*The README.md files on this repo were generated and beautified with Claude.*
