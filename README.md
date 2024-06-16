# Grayscale Ice Nucleation
 v1.4

 A terminal-user-interface (TUI) that detects and keeps track of grayscale intensity change of multiple circles using videos. Using the greatest change in intensity, the program is able to plot graphs showing the instance of freezing linked to time and temperature, and relate the radius size and freezing. Intended for analysis of ice-nucleating behaviour of ice-nucleating droplets under cryo-microscopy.

 Known compatibilities: Win10 | Win11

 To install: 
 - Pull the dist folder which contains the available versions for download. The .exe file is not a standalone file; it relies on _internal.

 How to use: 
 - Upon launching the .exe, the program will be a black console screen as it boots up. Subsequent usage may be done using the provided instructions within the program.

 Known issues:
 - Animated snowflake in loading screen does not properly render in Win10
 - Infinite loading screen when analyzing very short videos (single digit seconds)
 - Weirdly, able to process gifs and images when submitting as a 'video' file... negative 'video' properties will occur but analysis will work...
 - There is an issue in cross-matching temperature data files with unassociated videos... why?