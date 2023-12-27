cmake_minimum_required(VERSION 3.15)
project(lmshop VERSION 0.0.1 LANGUAGES CXX)
find_package(wt REQUIRED)
find_package(Boost REQUIRED)
add_compile_options(-Ofast -march=x86-64 -msse4.2 -std=c++2b)
add_executable(${PROJECT_NAME}
    dbase.cpp
    embeddableapp.cpp
    lmshop.cpp
    tools.cpp
    main.cpp)
target_link_libraries(${PROJECT_NAME}
    -lpthread
    -lssl
    -lcrypto
    -lcryptopp
    -lz
    -lboost_program_options
    -lboost_filesystem
    -lboost_thread
    -lwt
    -lwtdbo
    -lwtdbosqlite3
    -lwthttp)
foreach(ITEM "resources" "strings.xml" "strings-ru.xml" "wt_config.xml" "Dockerfile" "Readme.md" "embed.html")
  file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/${ITEM}" DESTINATION "${CMAKE_CURRENT_BINARY_DIR}")
endforeach()
