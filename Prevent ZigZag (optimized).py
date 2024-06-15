import math
abs_steering_threshold = 15  # Consider moving this to a global variable for further optimization

def reward_function(params):
  """
  This function calculates the reward for a Deepracer simulator step, penalizing zigzag behavior.

  Args:
      params (dict): Dictionary containing the following keys:
          distance_from_center (float): Distance of the car from the center line.
          track_width (float): Width of the track.
          steering_angle (float): Steering angle of the car.

  Returns:
      float: The reward value.
  """

  # Pre-calculate constants for efficiency
  MARKER_1 = 0.1 * params["track_width"]
  MARKER_2 = 0.25 * params["track_width"]
  MARKER_3 = 0.5 * params["track_width"]

  # Calculate distance reward based on pre-calculated markers
  distance_reward = 0.0
  if params["distance_from_center"] <= MARKER_1:
    distance_reward = 1.0
  elif params["distance_from_center"] <= MARKER_2:
    distance_reward = 0.5
  elif params["distance_from_center"] <= MARKER_3:
    distance_reward = 0.1
  else:
    distance_reward = 1e-3

  # Calculate steering penalty using absolute value and pre-defined threshold
  steering_penalty = 1.0 if math.fabs(params["steering_angle"]) <= abs_steering_threshold else 0.8

  # Combine rewards using multiplication for efficiency
  total_reward = distance_reward * steering_penalty

  return float(total_reward)
