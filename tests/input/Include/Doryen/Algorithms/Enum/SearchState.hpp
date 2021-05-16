#ifndef LIBTCOD_SEARCHSTATE_HPP
#define LIBTCOD_SEARCHSTATE_HPP

enum class SearchState : short
{
    NOT_INITIALISED,
    SEARCHING,
    SUCCEEDED,
    FAILED,
    OUT_OF_MEMORY,
    INVALID
};

#endif //LIBTCOD_SEARCHSTATE_HPP