cmake_minimum_required(VERSION 3.16)
project(Drawlingo VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Qt6 components
find_package(Qt6 REQUIRED COMPONENTS Core Widgets Network)
find_package(Qt6 COMPONENTS TextToSpeech QUIET)

# Enable automatic MOC, UIC, and RCC
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Source files
set(SOURCES
    src/main.cpp
    src/MainWindow.cpp
    src/DrawingCanvas.cpp
    src/SketchAnalyzer.cpp
)

set(HEADERS
    src/MainWindow.h
    src/DrawingCanvas.h
    src/SketchAnalyzer.h
)

# Create executable
add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

# Link Qt libraries
target_link_libraries(${PROJECT_NAME}
    Qt6::Core
    Qt6::Widgets
    Qt6::Network
)

# Link TextToSpeech if available
if(Qt6TextToSpeech_FOUND)
    target_link_libraries(${PROJECT_NAME} Qt6::TextToSpeech)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_QT_TEXTTOSPEECH)
endif()

# Include directories
target_include_directories(${PROJECT_NAME} PRIVATE src)

# Check if config.h exists and define HAVE_CONFIG_H
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/src/config.h")
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_CONFIG_H)
endif()

# Windows-specific settings
if(WIN32)
    set_target_properties(${PROJECT_NAME} PROPERTIES
        WIN32_EXECUTABLE TRUE
    )
endif()

