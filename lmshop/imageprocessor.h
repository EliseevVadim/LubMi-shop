#pragma once
#ifndef IMAGEPROCESSOR_H
#define IMAGEPROCESSOR_H

#include "dbase.h"
#include <memory.h>

class ImageProcessor final {
  public:
    static std::unique_ptr<Image> createProductImage(const std::string &file);
};

#endif // IMAGEPROCESSOR_H
