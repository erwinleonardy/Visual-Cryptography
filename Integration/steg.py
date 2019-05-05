import random, secrets
from PIL import Image, ImageDraw, ImageFont

# -- preset colors --
B = 0
W = 255

# -- File names -- 
hidden_name = 'img/ali.png'
share1_name = 'share1.png'
share2_name = 'share2.png'

# -- FUNCTIONS --
# converts a normal image to pure black.white pixels
# RGB converted to B/W based on which color they are closer to
def convertToBlack(img):
  img = img.convert('RGB')
  image = Image.new('1', img.size)

  # replace all pixels with either black or white pixels
  # if RGB values are closer to white, replace with white, else black
  for x in range(img.width):
    for y in range(img.height):
      tup = img.getpixel((x,y))
      if (tup[0] > 175 and tup[1] > 175 and tup[1] > 175):
        image.putpixel((x,y), W)
      else:
        image.putpixel((x,y), B)

  return image

# Open a normal image from filepath
def openImage(filename):
  img = Image.open(filename)
  img = convertToBlack(img)
  return img

# create source images
def createSource(size):
  choice = (W, B)
  color = random.choice(choice)

  img = Image.new('1', size, color)
  font = ImageFont.truetype("font/BebasNeue-Regular.ttf", 110)
  word = secrets.token_urlsafe(3)
  wordSize = font.getsize(word)
  cords = ((img.width - wordSize[0])//2,(img.height - wordSize[1])//2)

  draw = ImageDraw.Draw(img)
  draw.text(cords, word, (255 - color), font)
  return img

# open shares safely
def openShare(filename):
  return Image.open(filename)

# sets the subpixels within shares
def placePixels(share, tup, cords):
  x, y = cords[0], cords[1]

  share.putpixel((x, y), tup[0])
  share.putpixel((x + 1, y), tup[1])
  share.putpixel((x, y + 1), tup[2])
  share.putpixel((x + 1, y + 1), tup[3])

# If both source1, source2 pixels are black
def b1b2(hiddenColor):
  setA = ((W,B,B,B), (B,W,B,B), (B,B,W,B), (B,B,B,W))
  share1Pixel = random.choice(setA)
  
  # IF secret pixel is black: set share pixels with 3 black pixels each, 
  # such that when they overlap they form a set of 4 black pixels
  # ELIF secret pixel is white: set both share pixels with 3 of the same black pixels
  if (hiddenColor == B):
    share2Pixel = share1Pixel
    # as long as the set of 4 subpixels are not the same, condition is met
    while (share1Pixel == share2Pixel):
      share2Pixel = random.choice(setA)
  elif (hiddenColor == W):
    share2Pixel = share1Pixel

  return (share1Pixel, share2Pixel)

# If one source pixel is black, and the other white
def b1w2(hiddenColor):
  # IF secret pixel is black: source with black pixel will have 3 black pixels
  # while source with white pixel will have 2 black pixels, when overlapped they should
  # form a set of 4 black pixels
  # ELIF secret pixel is white: same as black, but when overlapped they should form a set
  # of 3 black pixels
  if (hiddenColor == B):
    share1Pixel = [B,B,B,B]
    share2Pixel = [W,W,W,W]

    blackOne = random.randint(0,3)
    share1Pixel[blackOne] = W # remove 1 random black pixel from share1
    blackTwo = blackOne
    while (blackTwo == blackOne):
      blackTwo = random.randint(0,3)

    share2Pixel[blackOne] = B # set overlapping black pixel
    share2Pixel[blackTwo] = B # set black pixel to meet condition

    share1Pixel = tuple(share1Pixel)
    share2Pixel = tuple(share2Pixel)
  elif (hiddenColor == W):
    setA = ((W,B,B,B), (B,W,B,B), (B,B,W,B), (B,B,B,W))
    share1Pixel = random.choice(setA)
    share2Pixel = list(share1Pixel)
    i_B = 0 # location of black pixel to remove
    for i in range(len(share2Pixel)):
      if (share2Pixel[i] == B):
        i_B = i

    share2Pixel[i_B] = W # remove a black pixel
    share2Pixel = tuple(share2Pixel)

  return (share1Pixel, share2Pixel)

# If both source1, source2 pixels are white
def w1w2(hiddenColor):
  setA = ((W,W,B,B), (B,B,W,W), (W,B,W,B), (B,W,B,W), (W,B,B,W), (B,W,W,B))
  share1Pixel = random.choice(setA)

  # IF secret pixel is black: both shares will have 2 black subpixels each, such that when
  # overlapped they form 4 black pixels
  # ELIF secret pixel is white: same as above, but when overlapped they should form a set
  # of 3 black pixels
  if (hiddenColor == B):
    share2Pixel = [B,B,B,B]
    # share2Pixels are opposite of share1Pixels
    for i in range(len(share1Pixel)):
      if (share1Pixel[i] == B):
        share2Pixel[i] = W
    
    share2Pixel = tuple(share2Pixel)
  elif (hiddenColor == W):
    share2Pixel = list(share1Pixel)
    i_B = 0 
    i_W = 0
    for i in range(len(share2Pixel)):
      if (share2Pixel[i] == B):
        i_B = i
      else:
        i_W = i

    share2Pixel[i_B] = W # a black pixel is replaced
    share2Pixel[i_W] = B # a white pixel is replaced
    share2Pixel = tuple(share2Pixel)

  return (share1Pixel, share2Pixel)

# based on the pixel colors from hidden, source1, source2,
# set the subpixels of the two new shares
def setSharePixels(hidden, source1, source2, share1, share2, cords):
  # get pixel color for the following, each either black or white
  hiddenPxl = hidden.getpixel(cords)
  source1Pxl = source1.getpixel(cords)
  source2Pxl = source2.getpixel(cords)

  # 4 possible combinations of source1, source2 pixel color,
  # each case results in a different set of subpixels in shares
  if (source1Pxl == B and source2Pxl == B):
    subPixels = b1b2(hiddenPxl)
  elif (source1Pxl == B and source2Pxl == W):
    subPixels = b1w2(hiddenPxl)
  elif (source1Pxl == W and source2Pxl == B):
    subPixels = b1w2(hiddenPxl)
    share1, share2 = share2, share1
  elif (source1Pxl == W and source2Pxl == W):
    subPixels = w1w2(hiddenPxl)

  subCords = (cords[0] * 2, cords[1] * 2)
  placePixels(share1, subPixels[0], subCords)
  placePixels(share2, subPixels[1], subCords)

# creates two new shares based on three images provided
def shareSplitter(hidden, source1, source2):
  # create new images for manipulation
  share1 = Image.new('1', (source1.width*2, source1.height*2))
  share2 = Image.new('1', (source1.width*2, source1.height*2))

  # x is horizontal, y is vertical; start from (0,0) 
  for x in range(hidden.width):
    for y in range(hidden.height):
      cords = (x, y) # pixel coordinates
      setSharePixels(hidden, source1, source2, share1, share2, cords)

  return share1, share2

# cleans reconstructed image to remove random noise
def cleanSecret(secret):
  clean = Image.new('RGBA', secret.size)

  for x in range(0, secret.width, 2):
    for y in range(0, secret.height, 2):
      sum = secret.getpixel((x, y)) + secret.getpixel((x + 1, y)) + \
              secret.getpixel((x, y + 1)) + secret.getpixel((x + 1, y + 1))
      if (sum > 0):
        alpha = ((W,W,W,0), (W,W,W,0), (W,W,W,0), (W,W,W,0))
      else:
        alpha = ((B,B,B,255), (B,B,B,255), (B,B,B,255), (B,B,B,255))
        
      placePixels(clean, alpha, (x, y))

  clean.show() # 5TH image to open is cleaned reconstructed image
  return clean

# reconstructs image based on the shares provided
def shareReconstructor(share1, share2):
  share1.paste(share2, mask = share1)
  share1.show() # 5TH image to open is reconstructed image
  secret = cleanSecret(share1)
  return secret

# -- MAIN -- 
if __name__ == "__main__":
  # [Opening Files]
  hidden = openImage(hidden_name)
  hidden.show() # 1ST image to open is the cleaned original image
  source1 = createSource(hidden.size)
  source2 = createSource(hidden.size)
  source1.show()
  source2.show()

  # [Generating Shares Phase]
  share1, share2 = shareSplitter(hidden, source1, source2)
  share1.show() # 2ND image to open is source1 share
  share2.show() # 3RD image to open is source1 share
  share1.save(share1_name)
  share2.save(share2_name)

  # [Reconstruction of Shares Phase]
  share1 = openShare(share1_name)
  share2 = openShare(share2_name)
  secret = shareReconstructor(share1, share2)
  cheque = Image.open('img/cheque.jpg')

  # [Paste Reconstructed Image On Cheque]
  cords = (1750, 750)
  cheque.paste(secret, cords, secret)
  cheque.show() # 6TH image to open is cheque/signature overlay
