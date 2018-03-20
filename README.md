# docker-bot
> Managing docker via a rocket bot.

The Current version starts a rocketchat server, the bot itself with [Hubot](https://hubot.github.com/docs/), and a python API which interacts with Docket API. You may use only the dockerbot python API to plug in any other chat bot (for discord, or whatever).



## Install & Deploy
- Make sure you have [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/) available on the host machine.
- Clone this repo `git clone https://github.com/Nakasar/docker-bot`.
- Move into the cloned repo directory `cd docker-bot`.
- Build and run the docker-compose file with `docker-compose up`.
- You're up to go !

> If you install docker-bot on a Virtual Machine, make sure to redirect port 3000 for rocketchat to work.



## Demo
- Access the rocketchat app at `127.0.0.1:3000` with any decent browser.
- Create a new accout named `dockerbot` with a fake email, password should be `dockerbot` and sign in.
- Log out.
- Create another account for you and sign in.
- Type `!docker help` to get started.



## Docs

### Imports
To import dockerbot and the desired systems :
```python
import dockerbot.<module>.<submodule>
```
#### Systems
| Module | System     | Description                                                          |
|--------|------------|----------------------------------------------------------------------|
| info   |            |                                                                      |
|        | containers | List containers, get container status...                             |
| logs   |            |                                                                      |
|        | containers | Logs all containers, errors, hook to error detection, search logs... |
| admin  |            |                                                                      |
|        | images     | Pull, build and run images.                                          |

### Dependancies
- dockerbot runs a REST API with [Flask](http://flask.pocoo.org/).
