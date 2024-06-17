import math
abs_steering_threshold = 20.0
direction_threshold = 10.0

def reward_function(params):

  reward = 1.0
  # Pre-calculate constants for efficiency
  MARKER_1 = 0.15 * params["track_width"]
  MARKER_2 = 0.30 * params["track_width"]
  MARKER_3 = 0.45 * params["track_width"]

  # Reward for all wheels on track
  if params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_1:
    reward = 1.0
  elif params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_2:
    reward = 0.5
  elif params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_3:
    reward = 0.01
  else:
    reward = 0.001

  # Calculate steering penalty using absolute value and pre-defined threshold
  reward *= 1.0 if math.fabs(params["steering_angle"]) <= abs_steering_threshold else 0.1

  # Reward for being close to the center of the track (negative for distance)
  #reward += -0.1 * min(1.0, params["closest_waypoints"] / 100.0)

  # Calculate the direction of the center line based on the closest waypoints
  next_point = waypoints[closest_waypoints[1]]
  prev_point = waypoints[closest_waypoints[0]]

  # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
  # Convert to degree
  # Calculate the difference between the track direction and the heading direction of the car
  direction_diff = abs(math.degrees(math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])) - params['heading'])
  if direction_diff > 180.0:
      direction_diff = 360.0 - direction_diff

  # Penalize the reward if the difference is too large
  if direction_diff > direction_threshold:
      reward *= 0.6

  # Reward for facing the direction of the track (cosine similarity between heading and ideal_heading)
"""  ideal_heading = math.radians(params.get("target_heading", 0))
  reward += -0.1 * math.cos(math.fabs(params["heading"] - ideal_heading)) """

  # Reward for making progress along the track
  reward += 0.95 * params["progress"]

  # Penalty for taking too many steps (encourages faster completion)
  reward += -0.6 * params["step"]

  return reward
