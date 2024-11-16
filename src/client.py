# REVAMP HOW THIS CLIENT IS HANDLED SO THAT IT ONLY HANDLES CLIENT DATA BUT ACTUAL PLAYER CONTROL IS WITHIN CLIENT_INTERFACE.PY AND FRONTEND IS RENDERED IN DISPLAY.PY

import socket
import json
import sys
import pygame
from display import init_display, handle_input, render, quit_display, load_sprite_frames
from enum import Enum


# Define Direction Enum
class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
    STATIC = "static"


HOST_IP_ADDRESS = "127.0.0.1"
PORT = 65432
SPRITE_SIZE = 90
FRAME_RATE = 15  # set 30 for smooth fps


def main():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST_IP_ADDRESS, PORT))  # connect to the server
        print(f"Connected to server at {HOST_IP_ADDRESS}:{PORT}")

        screen, clock = init_display()

        # Initially load sprite frames for the static state
        sprites = load_sprite_frames("./sprite/move/still/", SPRITE_SIZE)
        print(f"Loaded {len(sprites)} sprite frames...")

        # Initialize animation states for each player
        animation_states = {}

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Handle input and get movement deltas and direction
            dx, dy, direction = handle_input()

            # Only load new sprite frames if the direction has changed
            if direction != animation_states.get("last_direction", None):
                sprite_path = {
                    Direction.LEFT: "./sprite/move/left/",
                    Direction.RIGHT: "./sprite/move/right/",
                    Direction.UP: "./sprite/move/still/",
                    Direction.DOWN: "./sprite/move/still/",
                    Direction.STATIC: "./sprite/move/still/",
                }.get(
                    direction, "./sprite/move/still/"
                )  # Default to static if not matched

                sprites = load_sprite_frames(sprite_path, SPRITE_SIZE)
                print(
                    f"Loaded {len(sprites)} sprite frames for {direction.value} direction..."
                )

                if not sprites:
                    print(
                        f"Warning: No sprites loaded for {direction.value} direction!"
                    )
                else:
                    animation_states["last_direction"] = direction
                    animation_states[direction] = (
                        0  # Reset animation state for this direction
                    )

            # Prepare the movement input data to send to the server
            input_data = {"dx": dx, "dy": dy}
            client_socket.sendall(
                json.dumps(input_data).encode()
            )  # Send movement input to server

            # Receive and process the game state from the server
            data = client_socket.recv(1024)  # Receive game state from server
            positions = json.loads(data.decode())  # Process the game state

            # Render the game state with the updated sprite frames
            render(
                screen,
                positions,
                client_socket.fileno(),
                sprites,
                animation_states,
                direction,
            )

            # Cap the frame rate to control the game's speed
            clock.tick(FRAME_RATE)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Closing connection.")
        client_socket.close()
        quit_display()
        sys.exit()


if __name__ == "__main__":
    main()
