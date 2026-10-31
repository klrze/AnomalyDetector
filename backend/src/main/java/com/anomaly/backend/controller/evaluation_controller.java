package com.anomaly.backend.controller;

import com.anomaly.backend.entity.evaluation_log;
import com.anomaly.backend.service.evaluation_service;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/evaluations")
@RequiredArgsConstructor
public class evaluation_controller {

    private final evaluation_service evaluationService;

    @GetMapping("/channel/{channel}")
    public List<evaluation_log> getEvaluationsByChannel(@PathVariable String channel) {
        return evaluationService.getEvaluationsByChannel(channel);
    }
}