# Gurbani Automatic Speech Recognition

​This work was done as part of a Master's thesis project to achieve ASR of Gurbani. The final 
[Testset](https://archive.org/details/test.tar_202112) is available on archive.org. The archive includes the labelled audio and the test results.


To use the API make a POST request to http://localhost:8000 with the body: `{"audio": <audiodata>}`. Manyaudio formats are accepted but for best results stick to ~20s long audio.  Inferences done in the docker container are CPU only. If you wish to use GPU acceleration, you will have to setup an appropriate local development environment of the project with a gpu enabled pytorch environment. 



