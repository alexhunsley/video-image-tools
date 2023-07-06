# Frightful Thumbnails

This is a helper that makes it more convenient to work with thumbnail images generated from videos, especially in Finder (Mac OS) or Explorer (Windows).

(We'll assume Finder from now.)

# But what about Da Vinci/FCP/my favourite NLE?

They're great! But sometimes you don't want to faff around launching these tools, or don't have them available.

In those situations, thumbnails generated from videos are a handy preview tool that can be used in Finder by using Icon view mode.

# Show me an example

Suppose you have a video from your drone and you use something like `ffmpeg` to generate some jpg thumbnail images, one per second. For a 5 minute video that's 300 images.

If you visit the folder of images in Finder, you can turn on Icon view and see previews of all images. It's a little awkward to get the whole gist of the video,
as you have to scroll around, but it's doable.

Suppose now you have 20 drone videos (each 5 mins), and thumbnails made for each.

To preview them all, you can use the Search bar of Finder to find all .jpgs and view them as Icons. But now getting the gist of the videos' content is more annoying -- that's
6000 images now to scroll through.

Surely there's an easier way!

# So how can Frightful Thumbnails help?

This tool adds some special text to the end of each filename. Those additions let you use the Search bar to get a variable 'time stretching' effect on your thumbnails: you can view every other thumbnail,
every 4th thumbnail, 8th, and so on. 

This makes it very easy to get the gist of your video, or lots of videos.

# Example

Imagine you have thumbnail jpgs for a short video:

```
    dunsapie_loch_00001.jpg
    dunsapie_loch_00002.jpg
    dunsapie_loch_00003.jpg
    dunsapie_loch_00004.jpg
    dunsapie_loch_00005.jpg
    dunsapie_loch_00006.jpg
    dunsapie_loch_00007.jpg
    dunsapie_loch_00008.jpg
    dunsapie_loch_00009.jpg
    dunsapie_loch_00010.jpg
    dunsapie_loch_00011.jpg
```

After running Frightful Thumbnails, the files are renamed like this:

```
    dunsapie_loch_00001__b0000.jpg
    dunsapie_loch_00002__b.jpg
    dunsapie_loch_00003__b0.jpg
    dunsapie_loch_00004__b.jpg
    dunsapie_loch_00005__b00.jpg
    dunsapie_loch_00006__b.jpg
    dunsapie_loch_00007__b0.jpg
    dunsapie_loch_00008__b.jpg
    dunsapie_loch_00009__b000.jpg
    dunsapie_loch_00010__b.jpg
    dunsapie_loch_00011__b0.jpg
```

Those additions such as `b000` are known as 'scare codes' (geddit?).

They are designed so that you can search for `b0`, `b00`, `b000` etc in Finder to get 'time stretched' thumbnails.

For example:


| Search term  | Result            |
| ------------ | ----------------- |
|  `__b`         | Show every image  |
|  `__b0`        | Every 2nd image   |
|  `__b00`       | Every 4th image   |
|  `__b000`      | Every 8th image   |

And it works well for a Finder search that targets thumbnails for lots of videos -- in fact that's where it's quite powerful.

# How does this arcane magic work?

It uses a simple fact about incrementing binary numbers: collections of *at least* N 0s at the right hand side (LSBs) of the binary number have frequency `1/2^N`.

A chart makes this easier to see:

| 'M': image index  | M-1 as binary | Right-most 0s   | At least 1 0s? | At least 2 0? | At least 3 0s? | 
| ------------ | ------------------ | --------------- | -------------- | ------------- | -------------- |
|   1          |  0000              |  0000           |   Y            |   Y           |   Y            |
|   2          |  0001              |                 |                |               |                |
|   3          |  0010              |  0              |   Y            |               |                |
|   4          |  0011              |                 |                |               |                |
|   5          |  0100              |  00             |   Y            |   Y           |                |
|   6          |  0101              |                 |                |               |                |
|   7          |  0110              |  0              |   Y            |               |                |
|   8          |  0111              |                 |                |               |                |
|   9          |  1000              |  000            |   Y            |   Y           |   Y            |
|   10         |  1001              |                 |                |               |                |
|   11         |  1010              |  0              |   Y            |               |                |
|   12         |  1011              |                 |                |               |                |
|   13         |  1100              |  00             |   Y            |   Y           |                |
|   14         |  1101              |                 |                |               |                |



