package com.anomaly.backend.entity;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Entity
@Table(name = "experiment_log")
@Data
public class experiment_log {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "timestamp")
    private LocalDateTime timestamp;

    @Column(name = "window_size")
    private Integer windowSize;

    @Column(name = "hidden_dim")
    private Integer hiddenDim;

    @Column(name = "learning_rate")
    private Double learningRate;

    @Column(name = "epochs")
    private Integer epochs;

    @Column(name = "train_loss")
    private Double trainLoss;

    @Column(name = "val_loss")
    private Double valLoss;

    @Column(name = "f1_score")
    private Double f1Score;

    @Column(name = "notes")
    private String notes;
}