# Prompt: refresh the brand TOV guide (quarterly)

1. Re-crawl the site with `scripts/site_inventory.py ./site` to get a fresh `corpus.md`.
2. Rebuild `references/tov-guide.md` from the corpus, `diggerlid-meta-copy/references/voice-and-rules.md` and the customer voice in `usp-bank.md`:
   - Measure the stats again on the strongest on-brand pages: sentence length, % of short sentences, you:we ratio, exclamations, vocabulary counts.
   - Update the list of cross-page inconsistencies. Mark which earlier ones are now fixed.
   - Keep the 6-dimension rubric unless the evidence says to change it.
3. Every quote must exist verbatim in the inputs. No em dashes.
4. Report what changed since the last version.
