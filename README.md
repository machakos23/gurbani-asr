# Gurbani Automatic Speech Recognition

​This work was done as part of a Master's thesis project to perform Automatic Speech Recognition of Gurbani. The final 
[Testset](https://archive.org/details/test.tar_202112) is available on archive.org. This archive includes labelled audio and the test results. The ASR model was training on over a thousand hours of Gurbani audio.

## Usage 
- Retrieve the container: `docker pull machakos23/gurbani-asr`
- Run the container: `docker run -p 5000:5000 gurbani-asr`

## API 
To use the API make a POST request to http://localhost:5000 with the body: `{"audio": <audiodata>}`. Many audio formats are accepted but for best results stick to ~20s long audio.  Inferences done in the docker container are CPU only. If you wish to use GPU acceleration, you will have to setup an appropriate local development environment of the project with a gpu enabled pytorch environment. 



