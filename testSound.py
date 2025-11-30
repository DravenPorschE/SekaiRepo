import pygame

# Initialize mixer
pygame.mixer.init()

# Load the WAV file
pygame.mixer.music.load("beep-01a.wav")

# Play the file
pygame.mixer.music.play()

# Wait until it finishes playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
