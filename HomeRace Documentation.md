# HomeRace Documentation

## Socket Communication

````mermaid
stateDiagram-v2

select: Cart select
ready: All carts selected
starting: Countdown starts
started: Race starts
ended: Race ended
paused: Race paused

[*] --> select
select --> ready
ready --> starting
starting --> started
started --> ended
started --> paused
paused --> started
paused --> ended

ended --> [*]
````



| State  | Anfrage              | Antwort | Beschreibung |
| ------ | -------------------- | ------- | ------------ |
| select | connect(String name) | Race    |              |
|        |                      |         |              |
|        |                      |         |              |

````mermaid
classDiagram

Race <-- Player
Race <-- Cart
Player <|-- RacingPlayer

class Race {
	-String name
	-List<Player> players
	-String adminSessionId
	-List<Cart> carts
	-Boolean started
	-Boolean finished
	-Integer lapsToFinish
}

class Cart {
	-String ipAddress
	-String name
	-String imageUrl
}

class Player {
	-String name
	-String sessionId
	-String selectedCart
	-Integer laps
	-List<Timestap> times
}
````

## MQTT Communication

| Channel | Message | Description                                    |
| ------- | ------- | ---------------------------------------------- |
| /carts  | hey     | Search for all carts currently connected       |
|         | ho[ip]  | Response of all currently connected carts (1s) |
|         |         |                                                |

