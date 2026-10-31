package com.anomaly.backend.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "experiment_log")
public class experiment_log {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "channel")
    private String channel;

    @Column(name = "run_timestamp")
    private LocalDateTime runTimestamp;

    @Column(name = "window_size")
    private Integer windowSize;

    @Column(name = "batch_size")
    private Integer batchSize;

    @Column(name = "learning_rate")
    private Double learningRate;

    @Column(name = "epochs")
    private Integer epochs;

    @Column(name = "final_train_loss")
    private Double finalTrainLoss;

    @Column(name = "val_loss")
    private Double valLoss;

    @Column(name = "f1_score")
    private Double f1Score;

    @Column(name = "notes")
    private String notes;
}