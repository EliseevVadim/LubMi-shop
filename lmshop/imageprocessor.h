#pragma once
#ifndef IMAGEPROCESSOR_H
#define IMAGEPROCESSOR_H

#include "dbase.h"
#include <memory>
#include <expected>

class ImageProcessor final {
  public:
    static auto createProductImage(const std::string &file, bool primary) -> std::expected<std::unique_ptr<Image>, std::string>;
};

#endif // IMAGEPROCESSOR_H
