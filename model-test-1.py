import math

abs_steering_threshold = 15

def reward_function(params):
  MARKER_1 = 0.15 * params["track_width"]
  MARKER_2 = 0.30 * params["track_width"]
  MARKER_3 = 0.45 * params["track_width"]

  if params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_1:
    reward_all_wheels_on_track = 0.9
  elif params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_2:
    reward_all_wheels_on_track = 0.5
  elif params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_3:
    reward_all_wheels_on_track = 0.1
  else:
    reward_all_wheels_on_track = 1e-3

  steering_penalty = 1.0 if math.fabs(params["steering_angle"]) <= abs_steering_threshold else 0.9
  
  total_reward = reward_all_wheels_on_track * steering_penalty
  return total_reward