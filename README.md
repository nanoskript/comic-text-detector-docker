# comic-text-detector-docker

[Docker Hub](https://hub.docker.com/r/nanoskript/comic-text-detector)
| [Demo](https://comic-text-detector.nanoskript.dev/)

Docker service for <https://github.com/dmMaze/comic-text-detector>.

## Installation

```
docker run --publish $PORT:$PORT --env PORT=$PORT --detach nanoskript/comic-text-detector
```