import math

abs_steering_threshold = 20  # Consider moving this to a global variable for further optimization

def reward_function(params):
  """
  This function calculates the reward for a Deepracer simulator step.

  Args:
      params (dict): Dictionary containing the following keys:
          all_wheels_on_track (bool): Whether all wheels are on the track.
          closest_waypoints (int): Distance to the closest waypoint.
          heading (float): Car's heading in degrees.
          step (int): Current simulation step.
          progress (float): Progress along the track (0.0 to 1.0).

          distance_from_center (float): Distance of the car from the center line.
          track_width (float): Width of the track.
          steering_angle (float): Steering angle of the car.


  Returns:
      float: The reward value.
  """

  # Pre-calculate constants for efficiency
  MARKER_1 = 0.15 * params["track_width"]
  MARKER_2 = 0.30 * params["track_width"]
  MARKER_3 = 0.45 * params["track_width"]

  # Reward for all wheels on track
  if params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_1:
    reward_all_wheels_on_track = 1
  elif params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_2:
    reward_all_wheels_on_track = 0.5
  elif params["all_wheels_on_track"] and params["distance_from_center"] <= MARKER_3:
    reward_all_wheels_on_track = 0.01
  else:
    reward_all_wheels_on_track = 0.0

  # Calculate steering penalty using absolute value and pre-defined threshold
  steering_penalty = 1.0 if math.fabs(params["steering_angle"]) <= abs_steering_threshold else 0.1

  # Reward for being close to the center of the track (negative for distance)
  reward_closest_waypoints = -0.1 * min(1.0, params["closest_waypoints"] / 100.0)

  # Reward for facing the direction of the track (cosine similarity between heading and ideal_heading)
  ideal_heading = math.radians(params.get("target_heading", 0))
  reward_heading = -0.1 * math.cos(math.fabs(params["heading"] - ideal_heading))

  # Reward for making progress along the track
  reward_progress = 0.95 * params["progress"]

  # Penalty for taking too many steps (encourages faster completion)
  reward_step = -0.6 * params["step"]

  # Combine all reward components
  total_reward = (reward_all_wheels_on_track * steering_penalty) + reward_closest_waypoints + reward_heading + reward_progress + reward_step

  return total_reward  # Return the reward value without formatting
