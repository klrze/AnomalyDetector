package com.anomaly.backend.controller;

import com.anomaly.backend.entity.experiment_log;
import com.anomaly.backend.service.experiment_service;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/experiments")
@RequiredArgsConstructor
public class experiment_controller {

    private final experiment_service experimentService;

    @GetMapping("/channel/{channel}")
    public List<experiment_log> getExperimentsByChannel(@PathVariable String channel) {
        return experimentService.getExperimentsByChannel(channel);
    }
}