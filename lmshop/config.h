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

#define DRAG_LOCATION                     "Location"
#define DRAG_RACK                         "Rack"
#define DRAG_TIER                         "Tier"
#define DRAG_CELL                         "Cell"
#define DRAG_CONTAINER                    "Container"
#define DRAG_ALL                          DRAG_LOCATION, DRAG_RACK, DRAG_TIER, DRAG_CELL, DRAG_CONTAINER
#define SENS_SLEEP_TIME                   500ms

#endif // DEFINES_H
