include_guard(GLOBAL)

# Register any generated mechanism through MKPP's one compiled-artifact path. The generator emits
# one rates/jacobian source plus portable factorization and solve sources for every mechanism, so
# this intentionally has no header-only fallback for small mechanisms.
function(mkpp_add_compiled_mechanism target generated_dir mechanism)
  file(
    GLOB
    mechanism_sources
    CONFIGURE_DEPENDS
    "${generated_dir}/${mechanism}/rates.cpp"
    "${generated_dir}/${mechanism}/jacobian.cpp"
    "${generated_dir}/${mechanism}/solve.cpp"
    "${generated_dir}/${mechanism}/supernodal_factorize.cpp"
    "${generated_dir}/${mechanism}/supernodal_solve.cpp")
  # The unrolled reference factorization is emitted only with the reference backend flag, so include
  # its translation unit when present.
  if(EXISTS "${generated_dir}/${mechanism}/factorize.cpp")
    list(APPEND mechanism_sources "${generated_dir}/${mechanism}/factorize.cpp")
  endif()
  if(NOT mechanism_sources)
    message(
      FATAL_ERROR
        "FATAL ERROR: ${mechanism} has no generated compiled kernel sources in ${generated_dir}")
  endif()

  add_library(${target} STATIC ${mechanism_sources})
  target_compile_features(${target} PUBLIC cxx_std_23)
  # The kernel fragments include Kokkos headers for KOKKOS_INLINE_FUNCTION, so the translation units
  # need the same backend flags (e.g. OpenMP) as the main library.
  target_link_libraries(${target} PUBLIC Kokkos::kokkos)
endfunction()
