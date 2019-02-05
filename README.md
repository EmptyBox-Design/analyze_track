# analyze_track

Java used to analyze music sound waves within genres using processing for painting.

## Question

Is there any similarities between sound waves within genres of music?

## Background

On Spotify, Katy Perry's (pop singer) songs were within the Avenged Sevenfold (Rock/Metal) station. The station's composition was incredibly perplexing, and wondered if this is a mistake by Spotify's categorization algorithm, or could this be how a machine understands genres?

We categorize music based on how similar it sounds to other existing music. We rarely find a big metal breakdown in pop music, and when we do, it is surprising. We can alphabetize songs by their author(s), but could there exist another method of categorization, a categorization only a computer or machine would understand?

We as humans only understand certain sounds, based on numerous factors and components, from the physical space we are in, to how much water is in the air around us which would dampen the vibrations made by a given object. A machine can read the script from a sound file and the relay this information that we would otherwise miss. Wondering if a machine reading various sound files would categorize music differently than would, mixing Avenged Sevenfold with Katy Perry to a machine might make sense in ways that are foreign to us. A machine unless specified or programmed to delineate between rock and pop music might look at the musical portfolio on Spotify differently.

## Objective

Review 5 songs from each genre, then cross-compare their sound waves and see if there exist any verbose similarities between them. Focusing on the amplitude or height of each wavelength of sound and the distribution of amplitudes across a given song. The genre categorizations are derived from Spotify.

### Genres

* Country
* EDM
* Hip-Hop
* Indie
* Metal
* Punk
* Reggae
* Rock
* Rap
* Soul


### Inputs

Input data file in ```.mp3``` format

### Output

dump file of sound analysis in an array of objects.

#### Variables

| key | value | range | notes |
|------------------|--------|------| ------ |
| height | float | 0 - 10 | height of the band above 0. Each sound wavelength's amplitude is measured and normalized to floats between 0 -10 |
| i | index/band number | 0 - 512 | 512 java processing script requires a power of 2 for rendering, 512 provides adequete resolution while being relatively computational light |
| d | distribution of bands |  d > 0 | dimension is inclusive |
| d1 | distribution zone 1 | 0 - 127 | 0 <= d1 < d2 |
| d2 | distribution zone 2 | 128 - 256 | d1 < d2 < d3 |
| d3 | distribution zone 3 | 257 - 383 | d2 < d3 < d4 |
| d4 | distribution zone 4 | 384 - 512 | d3 < d4 <= 512 |

#### Wavelength

![wavelength-breakdown](/images/wavelength_breakdown.png)

### Dimension

![dimension-breakdown](images/dimension_breakdown.png)

#### output object

| key | value |
|------------------|--------|
| avgHeight | float |
| upperHeightLimit | float |
| lowerHeightLimit | float |
| distribution | object |
| d1 | float |
| d2 | float |
| d3 | float |
| d4 | float |

### Technical Libraries

* [Processing](https://processing.org/)

* [SoundFile](https://processing.org/reference/libraries/sound/FFT.html)

### Readings

Goldhagen, Sarah Williams. Welcome to Your World: How the Built Environment Shapes Our Lives. Harper, an Imprint of HarperCollinsPublishers, 2017.

Zumthor, Peter. Peter Zumthor: Atmospheres: Architectural Environments, Surrounding Objects. Birkhäuser, 2006.
