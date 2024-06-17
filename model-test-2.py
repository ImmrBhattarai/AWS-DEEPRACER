import math

ABS_STEERING_THRESHOLD = 15.0
DIRECTION_THRESHOLD = 10.0
MARKER_1 = 0.15
MARKER_2 = 0.30
MARKER_3 = 0.45
PROGRESS_WEIGHT = 0.95
STEP_PENALTY = -0.6

def reward_function(params):
    reward = 0.0

    # Pre-calculate constants outside the loop (efficiency)
    track_width = params["track_width"]
    distance = params["distance_from_center"]
    steering_angle = params["steering_angle"]
    progress = params["progress"]
    step = params["step"]

    # All wheels on track reward (vectorized for efficiency)
    all_wheels_on_track = params["all_wheels_on_track"]
    reward_on_track = [1.0, 0.55, 0.1, 0.001][
        (distance <= MARKER_1 * track_width) + (distance <= MARKER_2 * track_width) + (distance <= MARKER_3 * track_width)
    ] if all_wheels_on_track else [0.001]

    # Steering penalty (efficient calculation)
    reward_penalty = 1.0 if abs(steering_angle) <= ABS_STEERING_THRESHOLD else 0.1

    # Combined reward (vectorized and simplified)
    reward = reward_on_track[0] * reward_penalty + PROGRESS_WEIGHT * progress + STEP_PENALTY * step

    return reward
