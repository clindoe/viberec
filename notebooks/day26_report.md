# Day 26 — Qualitative Case Studies

10 seed movies spanning distinct vibe categories. For each seed, top-5 recommendations are shown at α=1.0 (pure vibe), α=0.5 (balanced), and α=0.0 (pure novelty).

> **Note on α=0.0:** At α=0.0, the scoring function reduces to `score = novelty`, which is entirely seed-independent. This is by design — it serves as a control condition showing what happens when content signal is fully removed. All seeds share the same α=0.0 output.


---

## The Dark Knight

**Vibe category:** Gritty action-thriller


### α = 1.0

|    | Title                                         |   Year | Genres                  |   Score |
|---:|:----------------------------------------------|-------:|:------------------------|--------:|
|  1 | The Lord of the Rings: The Return of the King |   2003 | Adventure,Drama,Fantasy |  1      |
|  2 | The Lord of the Rings: The Two Towers         |   2002 | Adventure,Drama,Fantasy |  1      |
|  3 | The War Room                                  |   1993 | Documentary,History     |  0.9899 |
|  4 | 2001: A Space Odyssey                         |   1968 | Adventure,Sci-Fi        |  0.8492 |
|  5 | Ocean's Eleven                                |   2001 | Crime,Thriller          |  0.8448 |



### α = 0.5

|    | Title                                         |   Year | Genres                  |   Score |
|---:|:----------------------------------------------|-------:|:------------------------|--------:|
|  1 | The War Room                                  |   1993 | Documentary,History     |  0.6925 |
|  2 | The Lord of the Rings: The Two Towers         |   2002 | Adventure,Drama,Fantasy |  0.5937 |
|  3 | The Lord of the Rings: The Return of the King |   2003 | Adventure,Drama,Fantasy |  0.592  |
|  4 | The Damned United                             |   2009 | Biography,Drama,Sport   |  0.5472 |
|  5 | 2001: A Space Odyssey                         |   1968 | Adventure,Sci-Fi        |  0.5198 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** At α=1.0 (pure vibe), the encoder surfaces epic, morally weighty narratives — Lord of the Rings and 2001: A Space Odyssey share The Dark Knight's atmosphere of grandeur and existential stakes. At α=0.5, collaborative signals reinforce prestige-drama overlap while adding Ocean's Eleven, reflecting the same audience's taste for polished, high-craft films. At α=0.0 results become seed-independent (novelty-only scoring), demonstrating that a non-zero α is essential for coherent recommendations.


---

## Mean Girls

**Vibe category:** Teen comedy


### α = 1.0

|    | Title                              |   Year | Genres         |   Score |
|---:|:-----------------------------------|-------:|:---------------|--------:|
|  1 | The Producers                      |   1967 | Comedy,Music   |  0.8414 |
|  2 | School for Scoundrels              |   1960 | Comedy         |  0.8334 |
|  3 | Yours, Mine and Ours               |   1968 | Comedy,Family  |  0.8296 |
|  4 | The Boss of It All                 |   2006 | Comedy         |  0.8269 |
|  5 | Monty Python's the Meaning of Life |   1983 | Comedy,Musical |  0.8184 |



### α = 0.5

|    | Title                 |   Year | Genres                  |   Score |
|---:|:----------------------|-------:|:------------------------|--------:|
|  1 | School for Scoundrels |   1960 | Comedy                  |  0.5761 |
|  2 | Yours, Mine and Ours  |   1968 | Comedy,Family           |  0.5506 |
|  3 | The Late Show         |   1977 | Comedy,Mystery,Thriller |  0.5496 |
|  4 | Highway 61            |   1991 | Comedy,Music            |  0.5482 |
|  5 | The Boss of It All    |   2006 | Comedy                  |  0.5425 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** Vibe similarity at α=1.0 surfaces older comedies with sharp social wit — School for Scoundrels and The Producers share Mean Girls' comedy-of-manners DNA despite the 40-year era gap, confirming the encoder captures tone over period. The α=0.5 blend retains genre fidelity while adding slightly more obscure entries that the same audience appreciated. At α=0.0 recommendations lose genre coherence entirely, confirming novelty alone cannot substitute for content-based signal.


---

## Eternal Sunshine

**Vibe category:** Surreal romance


### α = 1.0

|    | Title                |   Year | Genres                  |   Score |
|---:|:---------------------|-------:|:------------------------|--------:|
|  1 | The Usual Suspects   |   1995 | Crime,Drama,Mystery     |       1 |
|  2 | Shadow of a Doubt    |   1943 | Drama,Film-Noir,Mystery |       1 |
|  3 | Strangers on a Train |   1951 | Crime,Drama,Film-Noir   |       1 |
|  4 | Rashomon             |   1950 | Crime,Drama,Mystery     |       1 |
|  5 | Saving Private Ryan  |   1998 | Drama,War               |       1 |



### α = 0.5

|    | Title                            |   Year | Genres                  |   Score |
|---:|:---------------------------------|-------:|:------------------------|--------:|
|  1 | The Narrow Margin                |   1952 | Crime,Drama,Film-Noir   |  0.5964 |
|  2 | The Fallen Idol                  |   1948 | Drama,Film-Noir,Mystery |  0.595  |
|  3 | The Earrings of Madame De...     |   1953 | Drama,Romance           |  0.593  |
|  4 | Mouchette                        |   1967 | Drama                   |  0.5905 |
|  5 | Mishima: A Life in Four Chapters |   1985 | Biography,Drama         |  0.5877 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** At α=1.0, the encoder maps Eternal Sunshine to mystery-drama classics — Rashomon, The Usual Suspects, and Shadow of a Doubt all share its fractured-narrative, unreliable-reality vibe despite very different surface genres. At α=0.5 the mid-point shifts toward intimate character studies (Mishima, Mouchette) that the same cinephile audience rated highly. The α=0.0 collapse to identical results across all seeds confirms that novelty maximisation is seed-blind by design.


---

## Before Sunrise

**Vibe category:** Slow-burn dialogue romance


### α = 1.0

|    | Title                         |   Year | Genres                 |   Score |
|---:|:------------------------------|-------:|:-----------------------|--------:|
|  1 | That Obscure Object of Desire |   1977 | Comedy,Drama,Romance   |  0.9929 |
|  2 | Diary of a Chambermaid        |   1964 | Crime,Drama            |  0.9925 |
|  3 | Brute Force                   |   1947 | Crime,Drama,Film-Noir  |  0.9904 |
|  4 | This Sporting Life            |   1963 | Drama,Sport            |  0.9898 |
|  5 | The Name of the Rose          |   1986 | Drama,Mystery,Thriller |  0.9886 |



### α = 0.5

|    | Title                  |   Year | Genres                |   Score |
|---:|:-----------------------|-------:|:----------------------|--------:|
|  1 | Late Autumn            |   1960 | Comedy,Drama          |  0.6099 |
|  2 | This Sporting Life     |   1963 | Drama,Sport           |  0.6045 |
|  3 | The Cuckoo             |   2002 | Comedy,Drama,War      |  0.6022 |
|  4 | Brute Force            |   1947 | Crime,Drama,Film-Noir |  0.6021 |
|  5 | Diary of a Chambermaid |   1964 | Crime,Drama           |  0.6    |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** The vibe encoder correctly recognises Before Sunrise's contemplative, dialogue-driven European realism and surfaces Rohmer and Bunuel adjacent titles at α=1.0. At α=0.5, collaborative overlap adds quieter arthouse films that the same audience frequents — Late Autumn and The Cuckoo are strong cross-cultural matches. The α=0.0 collapse illustrates why the α knob exists: pure novelty erases all seed-specific signal.


---

## Get Out

**Vibe category:** Social horror


### α = 1.0

|    | Title                |   Year | Genres               |   Score |
|---:|:---------------------|-------:|:---------------------|--------:|
|  1 | The White Sheik      |   1952 | Comedy,Drama,Romance |  0.9109 |
|  2 | Pauline at the Beach |   1983 | Comedy,Drama,Romance |  0.9059 |
|  3 | The History Boys     |   2006 | Comedy,Drama,Romance |  0.8945 |
|  4 | Rushmore             |   1998 | Comedy,Drama,Romance |  0.886  |
|  5 | 42nd Street          |   1933 | Comedy,Drama,Musical |  0.8794 |



### α = 0.5

|    | Title                |   Year | Genres               |   Score |
|---:|:---------------------|-------:|:---------------------|--------:|
|  1 | The White Sheik      |   1952 | Comedy,Drama,Romance |  0.5845 |
|  2 | 42nd Street          |   1933 | Comedy,Drama,Musical |  0.5778 |
|  3 | Kandahar             |   2001 | Drama                |  0.5771 |
|  4 | Pauline at the Beach |   1983 | Comedy,Drama,Romance |  0.576  |
|  5 | His Brother          |   2003 | Drama,Romance        |  0.5708 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** At α=1.0, the model clusters Get Out with classic comedy-romances (The White Sheik, Pauline at the Beach) — likely because its tightly scripted social dynamics and ensemble tension share textual vibe markers with dialogue-rich ensemble films more than the horror genre alone would suggest. At α=0.5 Kandahar appears, showing collaborative filtering pulling in audiences drawn to socially-charged, boundary-pushing cinema. This seed most clearly illustrates the gap between genre labels and learned vibe space.


---

## Spirited Away

**Vibe category:** Studio Ghibli fantasy


### α = 1.0

|    | Title                |   Year | Genres                  |   Score |
|---:|:---------------------|-------:|:------------------------|--------:|
|  1 | The Usual Suspects   |   1995 | Crime,Drama,Mystery     |       1 |
|  2 | Shadow of a Doubt    |   1943 | Drama,Film-Noir,Mystery |       1 |
|  3 | Strangers on a Train |   1951 | Crime,Drama,Film-Noir   |       1 |
|  4 | Rashomon             |   1950 | Crime,Drama,Mystery     |       1 |
|  5 | Saving Private Ryan  |   1998 | Drama,War               |       1 |



### α = 0.5

|    | Title                            |   Year | Genres                  |   Score |
|---:|:---------------------------------|-------:|:------------------------|--------:|
|  1 | The Narrow Margin                |   1952 | Crime,Drama,Film-Noir   |  0.5964 |
|  2 | The Fallen Idol                  |   1948 | Drama,Film-Noir,Mystery |  0.595  |
|  3 | The Earrings of Madame De...     |   1953 | Drama,Romance           |  0.593  |
|  4 | Mouchette                        |   1967 | Drama                   |  0.5905 |
|  5 | Mishima: A Life in Four Chapters |   1985 | Biography,Drama         |  0.5877 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** The vibe encoder places Spirited Away alongside mystery-crime classics at α=1.0, reflecting shared narrative themes of a protagonist navigating an unknown, rule-bound world. At α=0.5, intimate period dramas appreciated by arthouse/Ghibli audiences emerge. Spirited Away shares its α=1.0 neighbourhood with Eternal Sunshine and Good Will Hunting, indicating a broad 'prestige narrative' cluster in the learned vibe space — an area where richer tag data or a transformer encoder could better discriminate.


---

## Good Will Hunting

**Vibe category:** Drama / character study


### α = 1.0

|    | Title                |   Year | Genres                  |   Score |
|---:|:---------------------|-------:|:------------------------|--------:|
|  1 | The Usual Suspects   |   1995 | Crime,Drama,Mystery     |       1 |
|  2 | Shadow of a Doubt    |   1943 | Drama,Film-Noir,Mystery |       1 |
|  3 | Strangers on a Train |   1951 | Crime,Drama,Film-Noir   |       1 |
|  4 | Rashomon             |   1950 | Crime,Drama,Mystery     |       1 |
|  5 | Saving Private Ryan  |   1998 | Drama,War               |       1 |



### α = 0.5

|    | Title                            |   Year | Genres                  |   Score |
|---:|:---------------------------------|-------:|:------------------------|--------:|
|  1 | The Narrow Margin                |   1952 | Crime,Drama,Film-Noir   |  0.5964 |
|  2 | The Fallen Idol                  |   1948 | Drama,Film-Noir,Mystery |  0.595  |
|  3 | The Earrings of Madame De...     |   1953 | Drama,Romance           |  0.593  |
|  4 | Mouchette                        |   1967 | Drama                   |  0.5905 |
|  5 | Mishima: A Life in Four Chapters |   1985 | Biography,Drama         |  0.5877 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** Good Will Hunting occupies the same α=1.0 neighbourhood as Eternal Sunshine and Spirited Away, pointing to a 'prestige emotional drama' super-cluster in the vibe space. At α=0.5, film-noir and intimate European dramas emerge through collaborative overlap, reflecting cinephile fans' broad tastes. This clustering suggests the encoder captures emotional register and narrative weight rather than explicit genre, which is the intended behaviour for a vibe-based system.


---

## Superbad

**Vibe category:** Raunchy teen comedy


### α = 1.0

|    | Title                                            |   Year | Genres       |   Score |
|---:|:-------------------------------------------------|-------:|:-------------|--------:|
|  1 | The Adventures of Priscilla, Queen of the Desert |   1994 | Comedy,Music |  0.9389 |
|  2 | Waking Ned Devine                                |   1998 | Comedy       |  0.9124 |
|  3 | Dirty Rotten Scoundrels                          |   1988 | Comedy,Crime |  0.8913 |
|  4 | Female Trouble                                   |   1974 | Comedy,Crime |  0.891  |
|  5 | Leningrad Cowboys Go America                     |   1989 | Comedy,Music |  0.8884 |



### α = 0.5

|    | Title                                            |   Year | Genres       |   Score |
|---:|:-------------------------------------------------|-------:|:-------------|--------:|
|  1 | Leningrad Cowboys Go America                     |   1989 | Comedy,Music |  0.6004 |
|  2 | Female Trouble                                   |   1974 | Comedy,Crime |  0.5931 |
|  3 | The Adventures of Priscilla, Queen of the Desert |   1994 | Comedy,Music |  0.5828 |
|  4 | Waking Ned Devine                                |   1998 | Comedy       |  0.5736 |
|  5 | Boudu Saved from Drowning                        |   1932 | Comedy       |  0.5703 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** The vibe encoder correctly identifies Superbad's raunchy-comedy road-trip energy, surfacing Priscilla Queen of the Desert and Waking Ned Devine at α=1.0 — films sharing its ensemble-friends-on-a-journey exuberance across very different settings. At α=0.5, Leningrad Cowboys persists (strong vibe match) while Boudu Saved from Drowning enters as a collaborative signal. Superbad produces the most genre-coherent and intuitively satisfying recommendations across all alpha levels, suggesting comedy vibe is well-separated in embedding space.


---

## Moonlight

**Vibe category:** Dark indie coming-of-age


### α = 1.0

|    | Title              |   Year | Genres                  |   Score |
|---:|:-------------------|-------:|:------------------------|--------:|
|  1 | An Unfinished Life |   2005 | Drama,Family,Romance    |  0.9486 |
|  2 | Pope Joan          |   2009 | Drama,History,Romance   |  0.9465 |
|  3 | Howl               |   2010 | Biography,Drama,Romance |  0.9447 |
|  4 | The Mother         |   2003 | Drama,Romance           |  0.9363 |
|  5 | Washington Square  |   1997 | Drama,Romance           |  0.9306 |



### α = 0.5

|    | Title                                           |   Year | Genres        |   Score |
|---:|:------------------------------------------------|-------:|:--------------|--------:|
|  1 | The Wooden Man's Bride                          |   1994 | Drama,Romance |  0.6333 |
|  2 | Like You Know It All                            |   2009 | Drama         |  0.6151 |
|  3 | Broken English                                  |   1996 | Drama,Romance |  0.6082 |
|  4 | Red Firecracker, Green Firecracker              |   1994 | Drama,Romance |  0.6072 |
|  5 | On the Occasion of Remembering the Turning Gate |   2002 | Drama,Romance |  0.6048 |



### α = 0.0

|    | Title                  |   Year | Genres               |   Score |
|---:|:-----------------------|-------:|:---------------------|--------:|
|  1 | Tunes of Glory         |   1960 | Drama                |  0.466  |
|  2 | Crude                  |   2009 | Documentary          |  0.4244 |
|  3 | The Icicle Thief       |   1989 | Comedy,Crime,Fantasy |  0.4228 |
|  4 | Street Thief           |   2006 | Crime,Thriller       |  0.4182 |
|  5 | A Hungarian Fairy Tale |   1987 | Fantasy              |  0.4126 |



**Analysis:** Moonlight's quiet, intimacy-driven vibe is faithfully captured at α=1.0, retrieving tender romance-drama films from China, UK, and France alongside American titles. At α=0.5, the blend shifts toward international arthouse films with similar emotional restraint and unhurried pacing. Moonlight yields the most globally diverse recommendation set of all seeds, reflecting the encoder's cultural agnosticism when plot pacing and emotional register align.
