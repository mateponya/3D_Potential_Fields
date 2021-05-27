from visual import Visual
import scenarios



### SELECT SCENARIO TO SIMULATE ###
# universe, animation_speed = scenarios.example()
universe, animation_speed = scenarios.spaceships2_collinear()
# universe, animation_speed = scenarios.spaceships2_cross()
# universe, animation_speed = scenarios.spaceships2_collinear()
# universe, animation_speed = scenarios.spaceships3_hex1()
# universe, animation_speed = scenarios.spaceships3_hex2()
# universe, animation_speed = scenarios.spaceships4_stell_octa()
# universe, animation_speed = scenarios.planets_in_line()
# universe, animation_speed = scenarios.planets_in_line_zigzag()
# universe, animation_speed = scenarios.multi_meteor_line()


# Simulate
trajectories, names, colors, sizes, goals, colors_goals = universe.simulate()

# Set up plotting
visual = Visual(trajectories, names, colors, sizes, goals, colors_goals,
                quality=8, save_animation=False, trace_length=-1, speed=animation_speed)
 
### DISPLAY STYLE ###

# 2D plot
# visual.plot2D()

# 3D plot
# visual.plot3D()

# 3D animation
visual.animate()

# Save 3D animation?
# visual.save_ani()