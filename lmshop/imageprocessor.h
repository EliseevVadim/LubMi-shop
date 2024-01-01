#pragma once
#ifndef IMAGEPROCESSOR_H
#define IMAGEPROCESSOR_H

#include "dbase.h"
#include <memory>
#include <expected>

class ImageProcessor final {
  public:
    static std::expected<std::unique_ptr<Image>, std::string>
    createProductImage(const std::string &file);
};

#endif // IMAGEPROCESSOR_H
