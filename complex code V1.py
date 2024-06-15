import math

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

  Returns:
      float: The reward value.
  """

  # Weighting factors for different reward components
  WEIGHT_ALL_WHEELS_ON_TRACK = 1.0
  WEIGHT_CLOSEST_WAYPOINTS = -0.1
  WEIGHT_HEADING = -0.1
  WEIGHT_PROGRESS = 1.0
  WEIGHT_STEP = -0.01

  # Reward for all wheels on track
  reward_all_wheels_on_track = WEIGHT_ALL_WHEELS_ON_TRACK if params["all_wheels_on_track"] else 0.0

  # Reward for being close to the center of the track (negative for distance)
  reward_closest_waypoints = WEIGHT_CLOSEST_WAYPOINTS * min(1.0, params["closest_waypoints"] / 100.0)

  # Reward for facing the direction of the track (cosine similarity between heading and ideal_heading)
  ideal_heading = math.radians(params.get("target_heading", 0))
  reward_heading = WEIGHT_HEADING * math.cos(math.fabs(params["heading"] - ideal_heading))

  # Reward for making progress along the track
  reward_progress = WEIGHT_PROGRESS * params["progress"]

  # Penalty for taking too many steps (encourages faster completion)
  reward_step = WEIGHT_STEP * params["step"]

  # Combine all reward components
  total_reward = reward_all_wheels_on_track + reward_closest_waypoints + reward_heading + reward_progress + reward_step

  return total_reward

# Example usage (assuming some values for the parameters)
params = {
  "all_wheels_on_track": True,
  "closest_waypoints": 20,
  "heading": 90,
  "step": 1000,
  "progress": 0.7,
  "target_heading": 180
}

reward = reward_function(params)
print(f"Reward: {reward}")

