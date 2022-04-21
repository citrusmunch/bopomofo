# -*- coding: utf-8 -*-
import pytest
import bopomofo


def test_application():
    assert bopomofo.to_bopomofo("注音") == "ㄓㄨˋ ㄧㄣ"
    assert bopomofo.to_bopomofo("注音", "、") == "ㄓㄨˋ、ㄧㄣ"
    assert bopomofo.to_bopomofo("注音", tones=False) == "ㄓㄨ ㄧㄣ"
    assert bopomofo.to_bopomofo("注音", first_tone_symbol=True) == "ㄓㄨˋ ㄧㄣˉ"
    assert bopomofo.to_bopomofo("English") == "English"
    assert bopomofo.to_bopomofo("English中文") == "English ㄓㄨㄥ ㄨㄣˊ"
    assert (
        bopomofo.to_bopomofo(
            "GitHub是一個透過Git進行版本控制的軟體原始碼代管服務", "", first_tone_symbol=True
        )
        == "GitHubㄕˋㄧˉㄍㄜˋㄊㄡˋㄍㄨㄛˋGitㄐㄧㄣˋㄒㄧㄥˊㄅㄢˇㄅㄣˇㄎㄨㄥˋㄓˋㄉㄜ˙ㄖㄨㄢˇㄊㄧˇㄩㄢˊㄕˇㄇㄚˇㄉㄞˋㄍㄨㄢˇㄈㄨˊㄨˋ"
    )


def test_extract_tone():
    cases = [
        ["fú", "fu", 2],
        ["wù", "wu", 4],
        ["shì", "shi", 4],
        ["yī", "yi", 1],
        ["tòu", "tou", 4],
        ["a", "a", 0],
    ]

    for case in cases:
        normalized, tone = bopomofo._single_pinyin_extarct_tone(case[0])
        assert normalized == case[1]
        assert tone == case[2]


def test_pinyin_to_bopomofo():
    cases = [
        ["fú", "ㄈㄨˊ"],
        ["wù", "ㄨˋ"],
        ["shì", "ㄕˋ"],
        ["yī", "ㄧ"],
        ["tòu", "ㄊㄡˋ"],
    ]

    for case in cases:
        assert bopomofo._single_pinyin_to_bopomofo(case[0], tones=True) == case[1]


def test_bopomofo_to_pinyin():
    cases = [
        ["fú", "ㄈㄨˊ"],
        ["wù", "ㄨˋ"],
        ["shì", "ㄕˋ"],
        ["yī", "ㄧ"],
        ["tòu", "ㄊㄡˋ"],
    ]

    for case in cases:
        assert bopomofo._single_bopomofo_to_pinyin(case[1], tones=True) == case[0]

    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_bopomofo_to_pinyin("ㄕㄕ")

    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_bopomofo_to_pinyin("ㄜㄜ")

    assert (
        bopomofo.bopomofo_to_pinyin(
            "GitHubㄕˋㄧˉㄍㄜˋㄊㄡˋㄍㄨㄛˋGitㄐㄧㄣˋㄒㄧㄥˊㄅㄢˇㄅㄣˇㄎㄨㄥˋㄓˋㄉㄜ˙ㄖㄨㄢˇㄊㄧˇㄩㄢˊㄕˇㄇㄚˇㄉㄞˋㄍㄨㄢˇㄈㄨˊㄨˋ"
        )
        == "GitHub shì yī gè tòu guò Git jìn xíng bǎn běn kòng zhì de ruǎn tǐ yuán shǐ mǎ dài guǎn fú wù"
    )
    assert (
        bopomofo.bopomofo_to_pinyin(
            "GitHubㄕˋㄧˉㄍㄜˋㄊㄡˋㄍㄨㄛˋGitㄐㄧㄣˋㄒㄧㄥˊㄅㄢˇㄅㄣˇㄎㄨㄥˋㄓˋㄉㄜ˙ㄖㄨㄢˇㄊㄧˇㄩㄢˊㄕˇㄇㄚˇㄉㄞˋㄍㄨㄢˇㄈㄨˊㄨˋ",
            tones=False,
        )
        == "GitHub shi yi ge tou guo Git jin xing ban ben kong zhi de ruan ti yuan shi ma dai guan fu wu"
    )


def test_to_pinyin():
    assert (
        bopomofo.to_pinyin("GitHub是一個透過Git進行版本控制的軟體原始碼代管服務", tones=True)
        == "GitHub shì yī gè tòu! guò! Git jìn xíng bǎn běn kòng zhì de ruǎn tǐ yuán shǐ mǎ dài guǎn fú wù"
    )
    assert (
        bopomofo.to_pinyin("GitHub是一個透過Git進行版本控制的軟體原始碼代管服務")
        == "GitHub shi yi ge tou guo Git jin xing ban ben kong zhi de ruan ti yuan shi ma dai guan fu wu"
    )


def test_invaild_inputs():
    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_pinyin_to_bopomofo("hee")

    with pytest.raises(bopomofo.PinyinParsingError):
        bopomofo._single_pinyin_to_bopomofo("vvv")
