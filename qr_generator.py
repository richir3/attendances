import qrcode

img = qrcode.make('WCHETEGACQ')
type(img)
img.save("qr_test.png")