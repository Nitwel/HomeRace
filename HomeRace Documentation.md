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

### Messages possible to the Server

| State                      | Message               | Response | Beschreibung |
| -------------------------- | --------------------- | -------- | ------------ |
| select                     | connect(String name)  | Race     |              |
| select                     | set_cart(String name) | boolean  |              |
| select -> ready / starting | ready()               |          |              |
| ready                      | unready()             |          |              |
| started                    | drive(Byte[2] drive)  |          |              |
|                            |                       |          |              |
|                            |                       |          |              |
|                            |                       |          |              |

### Messages from the Server

| State         | Message                            | Beschreibung                         |
| ------------- | ---------------------------------- | ------------------------------------ |
| select, ready | player_connected(Player player)    |                                      |
| select, ready | player_disconnected(Player player) |                                      |
| select, ready | player_ready(Player player)        |                                      |
| select, ready | player_unready(Player player)      |                                      |
| starting      | start_in(Integer timer)            | The countdown until the race starts. |
| started       | started(Timestamp time)            | The race has begun.                  |
| started       | lap_finished(Timestamp time)       |                                      |
| started       | race_finished(Timestamp time)      |                                      |

### Cart drive encoding

- Speed: [-100, 100] in % of speed
- Steering: [-100, 100] in % of steer-range (50deg) + 90deg

Which gives us a total of `201 x 201 = 40401 `Combinations. Which is well in the range of 16-bit (65536 Combinations).

To make it simpler to read out, we divide the 16-bit into 2 * 8-bit singed numbers, where the first byte is speed and the second is steering angle.



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

