---
name: Sindarin Language
description: This skill should be used when the user asks to "translate to Sindarin", "write in Elvish", "Sindarin grammar", "Elvish translation", "speak Sindarin", "Tolkien Elvish", or mentions Sindarin language, Grey-elven, or needs help with Elvish linguistics from Tolkien's legendarium.
version: 0.1.0
---

# Sindarin Language Skill

Sindarin is the Elvish language most commonly encountered in Tolkien's Middle-earth, spoken by the Grey-elves (Sindar) and later adopted by the Noldor in exile. This skill provides guidance for working with Sindarin translations, grammar, and composition.

## Purpose

Provide accurate Sindarin translations, grammatical guidance, and linguistic assistance for:
- Translating English phrases to Sindarin
- Understanding Sindarin grammar and mutations
- Composing names, phrases, and texts in Sindarin
- Explaining pronunciation and phonetics

## When to Use

Activate this skill when encountering requests involving:
- Translation requests to/from Sindarin or "Elvish"
- Questions about Sindarin grammar or structure
- Composition of Elvish names or phrases
- Tolkien linguistic matters relating to Grey-elven

## Core Concepts

### Consonant Mutations

Sindarin uses consonant mutations triggered by grammatical context. The main types:

1. **Soft Mutation (Lenition)** - Most common, triggered by articles, prepositions
2. **Nasal Mutation** - After words ending in nasal sounds
3. **Mixed Mutation** - After certain particles
4. **Stop Mutation** - After the article `i` (plural)

### Basic Grammar

- Word order: Generally SVO (Subject-Verb-Object)
- Adjectives typically follow nouns
- The definite article `i` (singular) / `in` (plural) triggers mutations
- Plurals formed through vowel changes (i-affection) or suffixes

### Phonetics

Sindarin pronunciation follows consistent rules:
- **C** always hard as in "cat"
- **G** always hard as in "get"
- **TH** as in "think" (voiceless)
- **DH** as in "this" (voiced)
- **CH** as in Scottish "loch"
- **R** always trilled
- Stress typically on penultimate syllable

## Workflow

To provide Sindarin assistance:

1. Identify the type of request (translation, grammar question, composition)
2. Consult `references/grammar.md` for grammatical rules
3. Consult `references/vocabulary.md` for word lookups
4. Apply appropriate mutations based on context
5. Provide pronunciation guidance when relevant

## Tengwar Script

Sindarin can be written in Latin script or in Tengwar, Tolkien's Elvish writing system. For displaying Tengwar:

### Quick Reference

- **CDN Font**: `https://fonts.cdnfonts.com/css/tengwar-annatar`
- **Transcription**: Use TengwarJS (`tengwar` npm package) or Tecendil
- **Inline SVG**: For environments without font loading (like Claude web)

### Rendering Options

1. **For HTML pages**: Link CDN font + use TengwarJS for transcription
2. **For Claude/inline**: Pre-render as SVG using `scripts/render-tengwar.js`
3. **Self-contained**: Embed font as base64 in HTML

### Resources

- **`references/tengwar.md`** - Complete Tengwar rendering guide
- **`scripts/render-tengwar.js`** - Node.js script for SVG generation
- **`templates/tengwar-page.html`** - HTML template with CDN fonts
- **`templates/tengwar-inline-svg.html`** - Self-contained SVG approach

## Additional Resources

### Reference Files

For detailed linguistic information, consult:
- **`references/grammar.md`** - Complete Sindarin grammar rules, mutations, and syntax
- **`references/vocabulary.md`** - English-Sindarin and Sindarin-English vocabulary
- **`references/tengwar.md`** - Tengwar script rendering for web

### Limitations

Sindarin is a constructed language with incomplete vocabulary. For words Tolkien never created:
- Use attested Sindarin roots where possible
- Note when a word is a neo-Sindarin reconstruction
- Prefer simpler constructions over uncertain neologisms
