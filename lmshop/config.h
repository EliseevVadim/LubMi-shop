#pragma once
#ifndef DEFINES_H
#define DEFINES_H

/**
 * maybe extern defines -- begin
 */

#ifndef STANDALONE_EMBEDDABLES
    #define STANDALONE_EMBEDDABLES          true
#endif

/**
 * maybe extern defines -- end
 */

#define AVAIL_LANGS                     "ru"
#define DEFAULT_LANG                    "en"
#define ANIM_DUR                        350

#define IMAGE_LINK_                     "resources/images/"
#define THUMBNAIL_SIZE                  150
#define THUMBNAIL_FILTER                LanczosFilter
#define CLR_BKG_HDR                     "#046a02"
#define CLR_HTEXT                       "#ffffff"
#define CLR_NTEXT                       "#ffff00"
#define CLR_BKG_0                       "#c4e09e"
#define CLR_BKG_1                       "#afcb8a"
#define CLR_BKG_2                       "#afcb8a"
#define CLR_FRAME                       CLR_BKG_HDR
#define CLR_INVIS                       "#00000000"
#define CONT_PANE_WIDTH                 "64mm"
#define INFO_WIDTH                      "100mm"
#define PADDING                         "4mm"

#endif // DEFINES_H
