
def sliding_window_tiles(img, tile_size=1024, overlap=200):
    h, w, _ = img.shape
    stride = tile_size - overlap
    tiles = []
    for y in range(0, h, stride):
        for x in range(0, w, stride):
            tile = img[y:y+tile_size, x:x+tile_size]
            tiles.append((tile, x, y))
    return tiles
